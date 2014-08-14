from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import models

from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from forms import FeedSearchForm

import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, "admin/home.html",{'user':request.user})

def about(request):
    return render(request, "about.html",{'user':request.user})

def welcome(request):
    return render(request, "welcome.html",{'user':request.user})

class FeedSearchView(FacetedSearchView):
    def __init__(self):
        super(FeedSearchView, self).__init__(form_class=FeedSearchForm)

    def _filter_facet_items(self, items, result_count=0):
        for item in items.items[:]:
            if item.is_selected:
                continue

            # Remove items which would return no results and items which do not
            # further restrict the query (i.e. would return the same number of
            # results when combined with the current query)
            if item.count == 0 or int(item.count) == int(result_count):
                items.items.remove(item)

    def extra_context(self):
        extra = super(FeedSearchView, self).extra_context()
        # trim down the facet_items: remove facets that don't supply extra constrictions
        facet_lists = self.form.searcher.facets
        for facet in facet_lists.facets:
            self._filter_facet_items(facet, result_count=len(self.results))

        extra['facet_items'] = facet_lists
        return extra
