from django.conf.urls import patterns, url, include
from django.conf import settings
from views import * 

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

sqs = SearchQuerySet() \
    .facet('breed', mincount=1, limit=10) \
    .facet('sex', mincount=1, limit=10) \
    .facet('taxon', mincount=1, limit=10) \

from django.contrib import admin

urlpatterns = patterns('',
    # Example:
    # (r'^feeddb/', include('feeddb.foo.urls')),

    (r'^static/(?P<path>.*)$', 
     'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^uploads/(?P<path>.*)$', 
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    #(r'^feed/', include(admin.site.urls)),
    (r'^$', 'feeddb.feed.views.index'),
    #(r'^$', include('feeddb.feed.urls')),

    # TODO: restore explorer URLs if they are desired. This line causes an
    # error when using the django debug toolbar.
    #(r'^explorer/', include('feeddb.explorer.urls')),

    (r'^about', 'feeddb.feed.views.about'),
    (r'^welcome', 'feeddb.feed.views.welcome'), 
    (r'^login$', login_view),
    (r'^logout$', logout_view),
    (r'^search/', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs)),
)

admin.autodiscover()
