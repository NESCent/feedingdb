from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
import models

from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from forms import FeedSearchForm

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

class FeedSearchView(FacetedSearchView):
    def __init__(self):
        super(FeedSearchView, self).__init__(form_class=FeedSearchForm)

    def __call__(self, request):
        self.request = request


        self.form = self.build_form()
        if request.method == 'POST':
            if request.POST.get('put_bucket', None):
                from feeddb.explorer.views import trial_search_put
                return trial_search_put(request)
            else:
                filters = self.form.searcher._clean_filters(request.POST)
                filters = sorted(filters, key=filter_key)
                q = request.POST.get('q', '')
                per_page = request.POST.get('per_page', '')
                if per_page:
                    filters.insert(0, ('per_page', per_page) )
                if q:
                    filters.insert(0, ('q', q) )

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

        return super(FeedSearchView, self).build_page()

    def extra_context(self):
        extra = super(FeedSearchView, self).extra_context()
        # trim down the facet_items: remove facets that don't supply extra constrictions
        facet_lists = self.form.searcher.facets
        for facet in facet_lists.facets:
            self._filter_facet_items(facet, result_count=len(self.results))

        extra['facet_items'] = facet_lists
        return extra
