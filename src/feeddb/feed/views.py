from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import models

from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from forms import FeedSearchForm

def index(request):
    return render(request, "admin/home.html",{'user':request.user})

def about(request):
    return render(request, "about.html",{'user':request.user})

def welcome(request):
    return render(request, "welcome.html",{'user':request.user})

class FeedSearchView(FacetedSearchView):
    def __init__(self):
        sqs = (SearchQuerySet()
            .facet('muscles', mincount=1, limit=10)
            .facet('muscles_part_of', mincount=1, limit=10)
            .facet('behaviorowl_primary_ancestors', mincount=1, limit=10)
            .facet('behaviorowl_secondary_ancestors', mincount=1, limit=10)
            .facet('behaviorowl_primary_part_of', mincount=1, limit=10)
            .facet('behaviorowl_secondary_part_of', mincount=1, limit=10)
        )

        super(FeedSearchView, self).__init__(form_class=FeedSearchForm, searchqueryset=sqs)
