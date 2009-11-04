from django.conf.urls.defaults import *
from feeddb import settings



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^feeddb/', include('feeddb.foo.urls')),

    (r'^static/(?P<path>.*)$', 
     'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^uploads/(?P<path>.*)$', 
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^feed/', include(admin.site.urls)),
    #(r'^$', include(admin.site.urls)),
    #(r'^$', include('feeddb.feed.urls')),
)

