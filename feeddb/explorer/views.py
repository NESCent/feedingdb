# VG: I suggest this usage for views.py: 
#  This is where back end (DB access & data massaging) and 
#  front end (presentation on web pages) are connected to each other. 
#  We will only keep the connecting code here. 
#  All non-trivial computations should be factored out separate modules. 

from django.http import HttpResponse
from django.views.generic.list_detail import object_detail
from feeddb.explorer.models import Bucket

def portal_page(request):
    return HttpResponse("TODO: the portal page")

def bucket_index(request):
    return HttpResponse("TODO: the list of this user's buckets")

def bucket_add(request):
    return HttpResponse("TODO: creating a new bucket")

def bucket_delete(request, id):
    return HttpResponse("TODO: deleting Bucket %s" % id)

# VG-claim: Finishing this view in the 1st pass needs only  
#     a detailed implementation of the bucket_detail.html template. 
#  However, we'll later need to improve efficiency of DB lookups. 
def bucket_detail(request, id):
    return object_detail(
        request, 
        queryset=Bucket.objects.all(), 
        object_id = id, 
        template_object_name = 'bucket', 
        template_name = 'explorer/bucket_detail.html',  #...which is the default
        )

def bucket_download(request, id):
    return HttpResponse("TODO: Specify all downloading parameters for Bucket %s and get a zip file with the data and metadata." % id )


def trial_search(request): 
    return HttpResponse("TODO: Search for trials and search results")

def trial_detail(request, id): 
    return HttpResponse("TODO: detailed information about Trial %s, including attributes of all its containers." % id)


