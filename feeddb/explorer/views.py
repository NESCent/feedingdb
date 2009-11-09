# VG: I suggest this usage for views.py: 
#  This is where back end (DB access & data massaging) and 
#  front end (presentation on web pages) are connected to each other. 
#  We will only keep the connecting code here. 
#  All non-trivial computations should be factored out separate modules. 

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.list_detail import object_detail
from feeddb.explorer.models import Bucket
from django.template import RequestContext, Template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic.simple import redirect_to
from django.contrib.auth import authenticate, login,logout
from feeddb.explorer.forms import *
from django.db.models import Q

def portal_page(request):
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'content': 'Welcome!'  })
    return render_to_response('explorer/index.html', c,
        mimetype="application/xhtml+xml")

def bucket_index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/explorer/login/?next=%s' % request.path)
    buckets = Bucket.objects.all()
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'buckets': buckets})
    return render_to_response('explorer/bucket_list.html', c,
        mimetype="application/xhtml+xml")

def bucket_add(request):
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'content': 'TODO: creating a new bucket'  })
    return render_to_response('explorer/base.html', c,
        mimetype="application/xhtml+xml")

def bucket_delete(request, id):
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'content': 'TODO: deleting Bucket %s' % id  })
    return render_to_response('explorer/base.html', c,
        mimetype="application/xhtml+xml")
    return HttpResponse("TODO: deleting Bucket %s" % id)

# VG-claim: Finishing this view in the 1st pass needs only  
#     a detailed implementation of the bucket_detail.html template. 
#  However, we'll later need to improve efficiency of DB lookups. 
def bucket_detail(request, id):
    bucket = Bucket.objects.get(pk=id)
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'bucket': bucket  })
    return render_to_response('explorer/bucket_detail.html', c,
        mimetype="application/xhtml+xml")

def bucket_download(request, id):
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'content': 'TODO: Specify all downloading parameters for Bucket %s and get a zip file with the data and metadata.' % id  })
    return render_to_response('explorer/base.html', c,
        mimetype="application/xhtml+xml")

def trial_search(request): 
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/explorer/login/?next=%s' % request.path)
    if request.method == 'POST': 
        query = Q(id__isnull=False)
        form = SearchTrailForm(request.POST) 
        if form.is_valid():
            species = form.cleaned_data['species']
            if species!=None and species != "":
                query = query & Q(session__experiment__study__subject__taxon__id__exact = species)
            muscle = form.cleaned_data['muscle']
            if muscle!=None and muscle != "":
                query = query & (Q(session__channels__setup__sensor__emgsensor__muscle__id__exact = muscle) | Q(session__channels__setup__sensor__sonosensor__muscle__id__exact = muscle) )
            behavior = form.cleaned_data['primary_behavior']
            if behavior!=None and behavior != "":
                query = query & Q(behavior_primary__id__exact = behavior) 
            food = form.cleaned_data['food_type']
            if food!=None and food != "":
                query = query & Q(food_type__icontains = food) 

            sensor = form.cleaned_data['sensor']
            if sensor!=None and sensor != "":
                sensor_query = Q()
                for tq in sensor:
                    sensor_query = sensor_query | Q(session__channels__setup__technique__id__exact = tq)
                query = query & sensor_query
            results= Trial.objects.filter(query).distinct()  
            
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'form': form, 'trials': results})
        return render_to_response('explorer/trial_list.html', c, mimetype="application/xhtml+xml")
    else:
        form= SearchTrailForm()
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'form': form})
        return render_to_response('explorer/search_trial.html', c, mimetype="application/xhtml+xml")

def trial_detail(request, id): 
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'content': 'TODO: detailed information about Trial %s, including attributes of all its containers.' % id })
    return render_to_response('explorer/base.html', c,
        mimetype="application/xhtml+xml")

def logout_view(request):
    logout(request)
    message = 'You have logged out.'
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': message})
    return render_to_response('explorer/index.html', c, mimetype="application/xhtml+xml")

def login_view(request):
    message = 'Please login'
    if request.method == 'GET':
        next = '/explorer'
        if request.GET.has_key('next'):
            next = request.GET['next'] 
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': message, 'next':next})
        return render_to_response('explorer/login.html', c, mimetype="application/xhtml+xml")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = '/explorer'
                if request.POST.has_key('next'):
                    next = request.POST['next'] 
                if not next is None and next !="": 
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect("/explorer")
            else:
                message = "The account is no longer active. Please try another account." 
        else:
            message = "No matched account found. Please try again."

        next = '/explorer'
        if request.GET.has_key('next'):
            next = request.GET['next'] 
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': message, 'next':next })
        return render_to_response('explorer/login.html', c, mimetype="application/xhtml+xml")



