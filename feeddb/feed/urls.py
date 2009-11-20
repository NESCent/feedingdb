from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^', 'feeddb.feed.views.index'),
)
