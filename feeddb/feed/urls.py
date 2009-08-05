from django.conf.urls.defaults import *
from feeddb import settings

urlpatterns = patterns('',
    (r'^', 'feeddb.feed.views.index'),
)
