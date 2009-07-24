from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', 'feeddb.feed.views.index'),
)
