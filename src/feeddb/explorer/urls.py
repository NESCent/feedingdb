# VG: I suggest discussing and coordinating most ideas about 
#     changing the design of URLs in this file. 

from django.conf.urls import patterns, url
from feeddb.explorer.views import * 
from django.conf import settings 

urlpatterns = patterns('',
  url(r'^$', portal_page),
  url(r'^bucket/$', bucket_index),
  url(r'^bucket/add/$', bucket_add),
  url(r'^bucket/(?P<id>\d+)/$', bucket_detail),
  url(r'^bucket/(?P<id>\d+)/delete/$', bucket_delete),
  url(r'^bucket/(?P<id>\d+)/download/$', bucket_download),
  url(r'^bucket/(?P<id>\d+)/remove_trials/$', bucket_remove_trials),
  url(r'^trial/search/$', trial_search),
  url(r'^trial/search/put/$', trial_search_put),
  url(r'^trial/(?P<id>\d+)/$', trial_detail, name='trial_detail'),
  url(r'^trial/(?P<id>\d+)/remove/(?P<bucket_id>\d+)/$', trial_remove),
  url(r'^trial/(?P<id>\d+)/put/$', trial_add, name='trial_add'),
  url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.EXPLORER_STATIC_ROOT}),
)
