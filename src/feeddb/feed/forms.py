from haystack.forms import FacetedSearchForm
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.query import RelatedSearchQuerySet
from inspector_panel import debug
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect

from feeddb.feed.models import Trial

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

        sqs = sqs.load_all()

        return sqs
