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
    (r'^happybrowser', 'feeddb.feed.views.happybrowser'),
    (r'^welcome', lambda r: HttpResponseRedirect('/')),
    (r'^login$', login_view),
    (r'^logout$', logout_view),
    (r'^search/', FeedSearchView()),
    (r'^profile/', UserOwnProfileChangeView.as_view()),
    url(r'^_clone_from_container/(?P<container_type>\w+)/(?P<container_pk>\d+)',
        ModelCloneView.as_view(), name='clone_from_container'),
    url(r'^_clone_subject_from_study/(?P<container_pk>\d+)',
        ModelCloneView.as_view(), name='clone_subject_from_study',
        kwargs={ 'container_type': 'study', 'clone_subject': True }),
    url(r'^_clone_study', ModelCloneView.as_view(), name='clone_study'),

    url(r'^ajax/add_taxon', TaxonModalAddView.as_view(), name='modal_add_taxon'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

