from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^', 'feed.views.index'),
)
