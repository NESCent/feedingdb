# VG: I suggest discussing and coordinating most ideas about 
#     changing the design of URLs in this file. 

from django.conf.urls.defaults import *
from feeddb.explorer.views import * 
from django.conf import settings 

urlpatterns = patterns('',
  (r'^$', portal_page),
  (r'^bucket/$', bucket_index),
  (r'^bucket/add/$', bucket_add),
  (r'^bucket/(?P<id>\d+)/$', bucket_detail),
  (r'^bucket/(?P<id>\d+)/delete/$', bucket_delete),
  (r'^bucket/(?P<id>\d+)/download/$', bucket_download),
  (r'^bucket/(?P<id>\d+)/remove_trials/$', bucket_remove_trials),
  (r'^trial/search/$', trial_search),
  (r'^trial/search/put/$', trial_search_put),
  (r'^trial/(?P<id>\d+)/$', trial_detail),
  (r'^trial/(?P<id>\d+)/remove/(?P<bucket_id>\d+)/$', trial_remove),
  (r'^trial/(?P<id>\d+)/put/$', trial_add),
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.EXPLORER_STATIC_ROOT}),
)