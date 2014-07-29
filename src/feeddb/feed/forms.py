from haystack.forms import FacetedSearchForm
from haystack.inputs import AutoQuery, Exact, Clean
from inspector_panel import debug

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class FeedSearchForm(FacetedSearchForm):
    
    def no_query_found(self):
        """
        Override no_query_found behavior to return all results when no keyword
        search is provided
        """
        return self.searchqueryset.all()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data.get('q'):
            q = self.cleaned_data['q']
            aq = AutoQuery(q)
            sqs = self.searchqueryset.filter_or(content=aq).filter_or(muscles=aq)
        else:
            sqs = self.searchqueryset.all()
        
        #sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

        return sqs
