# VG: I suggest discussing and coordinating most ideas about 
#     changing the design of URLs in this file. 

from django.conf.urls.defaults import *
from django.conf import settings

from feeddb.explorer.views import * 


urlpatterns = patterns('',
  (r'^$', portal_page),
  (r'^bucket/$', bucket_index),
  (r'^bucket/add/$', bucket_add),
  (r'^bucket/(?P<id>\d+)/$', bucket_detail),
  (r'^bucket/(?P<id>\d+)/delete/$', bucket_delete),
  (r'^bucket/(?P<id>\d+)/download/$', bucket_download),
  (r'^trial/search/$', trial_search),
  (r'^trial/(?P<id>\d+)/$', trial_detail),
)
