from django.conf.urls import patterns, url, include
from django.conf import settings
from django.http import HttpResponseRedirect
from views import * 
from feed.views import *

from haystack.query import SearchQuerySet

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^feeddb/', include('feeddb.foo.urls')),

    (r'^static/(?P<path>.*)$', 
     'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^uploads/(?P<path>.*)$', 
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    #(r'^feed/', include(admin.site.urls)),
    (r'^$', 'feeddb.feed.views.welcome'),
    #(r'^$', include('feeddb.feed.urls')),

    (r'^explorer/', include('feeddb.explorer.urls')),

    (r'^about', 'feeddb.feed.views.about'),
    (r'^welcome', lambda r: HttpResponseRedirect('/')), 
    (r'^login$', login_view),
    (r'^logout$', logout_view),
    (r'^search/', FeedSearchView()),
    (r'^clone_from_container/(?P<container_type>\w+)/(?P<container_pk>\d+)', ModelCloneView.as_view()),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

