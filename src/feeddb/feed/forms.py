from haystack.forms import FacetedSearchForm
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.query import RelatedSearchQuerySet
from inspector_panel import debug
from django import forms
from django.forms.fields import ChoiceField, BooleanField
from django.forms.widgets import RadioSelect
from django.core.urlresolvers import reverse

from feeddb.feed.models import Trial, Session, Experiment, Subject, Study

from faceted_search.searcher import Searcher

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

my_facet_config = {
    'fields': {
        'analoc': { 'label': 'Anatomical Location' },
        'behaviorowl_primary_ancestors': { 'label': 'Primary Behavior' },
        'taxon': { 'label': 'Species' },
        'food_type': { 'label': 'Food Type' },
        'techniques': { 'label': 'Sensor Type' },
    }
}

class ModelCloneForm(forms.Form):
    source = forms.ModelChoiceField(queryset=None)
    recurse = forms.BooleanField()

    def __init__(self, container=None, *args, **kwargs):
        self.clone_subject = kwargs.pop('clone_subject', False)

        super(ModelCloneForm, self).__init__(*args, **kwargs)

        ContainerModel = type(container)

        if ContainerModel == Session:
            qs = Trial.objects.filter(session=container)
        elif ContainerModel == Experiment:
            qs = Session.objects.filter(experiment=container)
        elif ContainerModel == Study:
            if self.clone_subject:
                qs = Subject.objects.filter(study=container)
            else:
                qs = Experiment.objects.filter(study=container)
        elif container == None:
            qs = Study.objects.all()
        else:
            raise ValueError("ModelCloneForm does not support container model type %s" % ContainerModel)

        self.fields['source'].queryset = qs
        self.container = container

    def action_url(self):
        "Get url for action attribute of form tag. See ../urls.py"
        if self.container == None:
            return reverse('clone_study')
        elif self.clone_subject:
            kwargs = {
                'container_pk': self.container.pk,
            }
            return reverse('clone_subject_from_study', kwargs=kwargs)
        else:
            kwargs = {
                'container_type': type(self.container).__name__.lower(),
                'container_pk': self.container.pk,
            }
            return reverse('clone_from_container', kwargs=kwargs)

    def clean(self):
        cleaned_data = super(ModelCloneForm, self).clean()
        if self.data['recurse'] == 'do_not':
            cleaned_data['recurse'] = False
        elif self.data['recurse'] == 'do':
            cleaned_data['recurse'] = True
        return cleaned_data

    @classmethod
    def factory(cls, modeladmin, request):
        context = {
            'opts': modeladmin.model._meta,
            'request': request
        }
        from feeddb.feed.templatetags.upload_status import get_current_containers
        containers = get_current_containers(context)
        try:
            # move down the tree until they don't exist anymore
            container = None
            container = containers['study']
            container = containers['experiment']
            container = containers['session']
        except KeyError:
            pass

        if context['opts'].model_name == 'subject':
            return cls(container=container, clone_subject=True)
        else:
            return cls(container=container)

class FeedSearchForm(FacetedSearchForm):
    per_page = ChoiceField(
        choices=[(n, n) for n in (10, 30, 50, 100, 200)],
        initial=10,
        widget=RadioSelect(),
    )

    def __init__(self, GET, *args, **kwargs):
        # Save all GET parameters in case they match facets and not form fields
        self.filters = GET

        super(FeedSearchForm, self).__init__(GET, *args, **kwargs)
        self.searcher = Searcher(model=Trial, facets=my_facet_config, queryset=RelatedSearchQuerySet())

    def no_query_found(self):
        """
        Override no_query_found behavior to return all results when no keyword
        search is provided
        """
        return self.searchqueryset.all()

    def search(self):
        # Get keywords from form, defaulting to empty string
        try:
            q = self.cleaned_data['q']
        except (AttributeError, KeyError): # if self.cleaned_data doesn't exist
            q = ''

        sqs = self.searcher.search(filters=self.filters, keywords=q)

        sqs = sqs.order_by('taxon')

        sqs = sqs.load_all()

        return sqs
