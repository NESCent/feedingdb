from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse
from django.db.models.loading import get_model
from django.utils.http import urlencode
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from models import Study, Experiment, Session, Trial, Taxon

from django.contrib import messages

from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from forms import FeedSearchForm, ModelCloneForm

from feeddb.explorer.models import Bucket
from django.views.generic.edit import FormView, CreateView

import logging
logger = logging.getLogger(__name__)

FACET_SORT_ORDER = getattr(settings, 'FACET_SORT_ORDER', [])

def index(request):
    return render(request, "admin/home.html",{'user':request.user})

def about(request):
    return render(request, "about.html",{'user':request.user})

def welcome(request):
    return render(request, "welcome.html",{'user':request.user})

def filter_key(f):
    """ See facet_key() in facets.py """
    try:
        index = FACET_SORT_ORDER.index(f[0])
    except ValueError:
        index = 0

    return (index, f[0], f[1])

class TaxonModalAddView(CreateView):
    model = Taxon
    template_name_suffix = '_modal_create_form'
    fields = ['genus', 'species', 'common_name']

    def form_valid(self, form):
        form.save()
        context = {
            'object': form.instance,
            'model': self.model,
            'opts': self.model._meta,
        }
        template_name = 'feed/' + self.model.__name__.lower() + self.template_name_suffix + '_success.html'
        return SimpleTemplateResponse(template_name, context)

class ModelCloneView(FormView):
    """
    This view provides a POST endpoint for the ModelCloneForm, which is only
    accessible on model add pages via a modal form.

    The form should always succeed; it redirects to the new object.
    """

    form_class = ModelCloneForm
    template_name = 'clone_form.html'
    http_method_names = ['post']

    def dispatch(self, request, container_type=None, container_pk=None, clone_subject=False, *args, **kwargs):
        self.container_type = container_type
        self.container_pk = container_pk
        self.clone_subject = clone_subject
        return super(ModelCloneView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ModelCloneView, self).get_form_kwargs()
        if self.container_type and self.container_pk:
            pk = long(self.container_pk)
            kwargs['container'] = get_model('feed', self.container_type).objects.get(pk=pk)
        elif self.container_type == None:
            kwargs['container'] = None
        kwargs['clone_subject'] = self.clone_subject
        return kwargs

    def _make_message(self, source, recurse):
        if type(source) == Study:
            if recurse:
                return 'New study created. Please edit the study and all its experiments, sessions, and trials.'
            else:
                return 'New study created. Please edit the study.'
        elif type(source) == Experiment:
            if recurse:
                return 'New experiment created. Please edit the experiment and all its sessions and trials.'
            else:
                return 'New experiment created. Please edit the experiment.'
        elif type(source) == Session:
            if recurse:
                return 'New session created. Please edit the session and all its trials.'
            else:
                return 'New session created. Please edit the session.'
        elif type(source) == Trial:
            return 'New trial created. Please edit the trial.'

    def form_valid(self, form):
        from cloning import clone_supported_object
        source = form.cleaned_data['source']
        recurse = form.cleaned_data['recurse']
        clone_supported_object(source, recurse=recurse)
        self.dest = source

        messages.info(self.request, self._make_message(source, recurse))

        return super(ModelCloneView, self).form_valid(form)

    def get_success_url(self):
        "Redirect to newly created object's edit form when successful"
        return self.dest.get_absolute_url(change=True) + '?is_clone'

def clone_view(request, container_type, container_pk):
    container = get_model('feed', container_type).objects.get(pk=container_pk)

    if request.method == 'POST':
        form = ModelCloneForm(container, request.POST)
    else:
        form = ModelCloneForm(container)

class FeedSearchView(FacetedSearchView):
    def __init__(self):
        super(FeedSearchView, self).__init__(form_class=FeedSearchForm)

    def __call__(self, request):
        self.request = request

        self.form = self.build_form()

        # If we were POSTed to, guess the appropriate form. If it's the trial
        # bucket form, use that gross view function. If it's the search form,
        # we canonicalize the query and redirect to a GET request.
        if request.method == 'POST':
            if request.POST.get('put_bucket', None):
                from feeddb.explorer.views import trial_search_put
                response = trial_search_put(request)
                if isinstance(response, HttpResponseRedirect):
                    return response

                # If we're not using that response, reset the message queue
                # that was emptied when rendering that response.
                #
                # FIXME: rewrite the trial_search_put view as a Form class
                storage = messages.get_messages(request)
                storage.used = False

            q = request.POST.get('q', '')
            old_q = request.POST.get('old_q', '')
            if q == old_q:
                # get facet filters in sorted order
                filters = self.form.searcher._clean_filters(request.POST)
                filters = sorted(filters, key=filter_key)
            else:
                # if user changed search text, reset all filters
                filters = []

            # Add keywords and per_page arguments
            per_page = request.POST.get('per_page', '')
            if per_page:
                filters.insert(0, ('per_page', per_page) )
            if q:
                filters.insert(0, ('q', q) )

            # Get our own URL, add filters to query string, and redirect.
            url = reverse(self)
            if len(filters):
                url += '?' + urlencode(filters)

            return redirect(url)

        self.query = self.get_query()
        self.results = self.get_results()
        return self.create_response()

    def _filter_facet_items(self, items, result_count=0):
        for item in items.items[:]:
            if item.is_selected:
                continue

            # Remove items which would return no results and items which do not
            # further restrict the query (i.e. would return the same number of
            # results when combined with the current query)
            if item.count == 0 or int(item.count) == int(result_count):
                items.items.remove(item)

    def build_page(self):
        try:
            self.results_per_page = int(self.form.cleaned_data['per_page'])
        except (AttributeError, KeyError): # cleaned_data doesn't exist
            pass

        (paginator, page) = super(FeedSearchView, self).build_page()

        if page.has_next():
            page.next_page_params = self.pager_params(page.next_page_number())
        if page.has_previous():
            page.previous_page_params = self.pager_params(page.previous_page_number())

        paginator.first_page_params = self.pager_params(1)

        return (paginator, page)

    def pager_params(self, page_no):
        params = self.request.GET.copy()

        # Remove page parameter for first page
        if page_no == 1 and params.get('page', False):
            params.pop('page')
        else:
            params['page'] = page_no

        return params.urlencode()

    def extra_context(self):
        extra = super(FeedSearchView, self).extra_context()
        # trim down the facet_items: remove facets that don't supply extra constrictions
        facet_list = self.form.searcher.facets
        for facet in facet_list.facets:
            self._filter_facet_items(facet, result_count=len(self.results))

        extra['facet_items'] = facet_list
        from feeddb.explorer.views import get_user_buckets
        extra['available_buckets'] = get_user_buckets(self.request)
        return extra
