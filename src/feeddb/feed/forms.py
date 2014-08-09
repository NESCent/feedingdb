from haystack.forms import FacetedSearchForm
from haystack.inputs import AutoQuery, Exact, Clean
from inspector_panel import debug

from feeddb.feed.models import Trial

from faceted_search.searcher import Searcher

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class FeedSearchForm(FacetedSearchForm):
    facets = { 
        'fields': { 
            'muscles': { 'label': 'Muscles' },
            'muscles_part_of': { 'label': 'Part of Muscles' },
        }
    }


    def __init__(self, GET, *args, **kwargs):
        try:
            self.filters = GET.dict()
        except AttributeError:
            self.filters = {}
        super(FeedSearchForm, self).__init__(GET, *args, **kwargs)
        self.searcher = Searcher(model=Trial, facets=FeedSearchForm.facets)
    
    def no_query_found(self):
        """
        Override no_query_found behavior to return all results when no keyword
        search is provided
        """
        return self.searchqueryset.all()

    def search(self):
        # Get keywords from form, or not at all
        try:
            q = self.cleaned_data['q']
        except AttributeError:
            q = ''

        sqs = self.searcher.search(filters=self.filters, keywords=q)
        
        if self.load_all:
            sqs = sqs.load_all()

        return sqs
