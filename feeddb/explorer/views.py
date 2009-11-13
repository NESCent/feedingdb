# VG: I suggest this usage for views.py: 
#  This is where back end (DB access & data massaging) and 
#  front end (presentation on web pages) are connected to each other. 
#  We will only keep the connecting code here. 
#  All non-trivial computations should be factored out separate modules. 

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_detail
from django.template import RequestContext, Template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic.simple import redirect_to
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.utils.html import escape
from feeddb.explorer.models import *
from feeddb.feed.models import *
from feeddb.explorer.forms import *


def portal_page(request):
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'content': 'Welcome!'  })
    return render_to_response('explorer/index.html', c,
        mimetype="application/xhtml+xml")

def bucket_index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/explorer/login/?next=%s' % request.path)
    buckets = Bucket.objects.filter(created_by=request.user)
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
                query = query & Q(session__experiment__subject__taxon__id__exact = species)
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
                    if tq!=None and tq != "":
                        sensor_query = sensor_query | Q(session__channels__setup__technique__id__exact = tq)
                        query = query & sensor_query
            results= Trial.objects.filter(query).distinct()  
            
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'form': form, 'trials': results})
        return render_to_response('explorer/trial_list.html', c, mimetype="application/xhtml+xml")
    else:
        form= SearchTrailForm()
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'form': form})
        return render_to_response('explorer/search_trial.html', c, mimetype="application/xhtml+xml")

def trial_search_put(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/explorer/login/?next=%s' % request.path)
    #check if any trial selected
    trial_selected = []
    for item in request.POST.items():
        if(item[1]=="on"):
            trial_selected.append(item[0])
    if len(trial_selected) ==0:
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'no trial selected.'})
        return render_to_response('explorer/base.html', c, mimetype="application/xhtml+xml")
    #check if new bucket selected
    bucket = None
    bucket_selected = request.POST['bucket']
    if bucket_selected ==None or bucket_selected =="":
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'no bucket selected.'})
        return render_to_response('explorer/base.html', c, mimetype="application/xhtml+xml")
    if request.POST['bucket']!='add new bucket':
        bucket = Bucket.objects.get(pk=bucket_selected)
    else: 
        new_bucket_name=request.POST['new_bucket_name']
        if new_bucket_name==None and new_bucket_name =="":
            c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'no new bucket name specified.'})
            return render_to_response('explorer/base.html', c, mimetype="application/xhtml+xml")
        else:
            bucket = Bucket()
            bucket.created_by = request.user
            bucket.title = new_bucket_name
            bucket.save()
    #add trials to the bucket
    for trial_id in trial_selected:
        trial = Trial.objects.get(pk=trial_id)
        assocs = TrialInBucket.objects.filter(Q(trial__id__exact=trial_id) & Q(bin__id__exact=bucket.id))
        if len(assocs) ==0:
            assoc = TrialInBucket(trial=trial, bin = bucket)
            assoc.save()
    
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'successfully put the selected trials to the bucket', 'bucket':bucket})
    return render_to_response('explorer/bucket_detail.html', c, mimetype="application/xhtml+xml")

def trial_detail(request, id): 
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/explorer/login/?next=%s' % request.path)
    try:
        trial = Trial.objects.get(pk=id)
    except Trial.DoesNotExist:
        c = RequestContext(request, {'title': 'Error | FeedDB Explorer', 'message': 'Trial with primary key %(key)r does not exist.' % {'key': escape(id)}})
        return render_to_response('explorer/error.html', c, mimetype="application/xhtml+xml")
    c = RequestContext(request, {'title': 'Trial Detail | FeedDB Explorer', 'trial': trial})
    return render_to_response('explorer/trial_detail.html', c, mimetype="application/xhtml+xml")

def trial_remove(request, id, bucket_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/explorer/login/?next=%s' % request.path)
    try:
        trial = Trial.objects.get(pk=id)
    except Trial.DoesNotExist:
        c = RequestContext(request, {'title': 'Error | FeedDB Explorer', 'message': 'Trial with primary key %(key)r does not exist.' % {'key': escape(id)}})
        return render_to_response('explorer/error.html', c, mimetype="application/xhtml+xml")

    try:
        bucket = Bucket.objects.get(pk=bucket_id)
    except Bucket.DoesNotExist:
        c = RequestContext(request, {'title': 'Error | FeedDB Explorer', 'message': 'Bucket with primary key %(key)r does not exist.' % {'key': escape(bucket_id)}})
        return render_to_response('explorer/error.html', c, mimetype="application/xhtml+xml")
    
    try:
        assoc = TrialInBucket.objects.filter(Q(trial__id__exact=id) & Q(bin__id__exact=bucket_id))
    except TrialInBucket.DoesNotExist:
        c = RequestContext(request, {'title': 'Error | FeedDB Explorer', 'message': 'Trial: %s is not in the bucket: %s.' % (trial, bucket)})
        return render_to_response('explorer/error.html', c, mimetype="application/xhtml+xml")
    
    assoc.delete()
    c = RequestContext(request, {'title': 'Trial Detail | FeedDB Explorer', 'trial':trial, 'message':'Trial: %s has been successfully removed from the bucket: %s.' % (trial, bucket)})
    return render_to_response('explorer/trial_detail.html', c, mimetype="application/xhtml+xml")

def trial_add(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/explorer/login/?next=%s' % request.path)
    if request.method =='POST':
        try:
            trial = Trial.objects.get(pk=id)
        except Trial.DoesNotExist:
            c = RequestContext(request, {'title': 'Error | FeedDB Explorer', 'message': 'Trial with primary key %(key)r does not exist.' % {'key': escape(id)}})
            return render_to_response('explorer/error.html', c, mimetype="application/xhtml+xml")
        
        if request.POST['bucket_id']!='add new bucket':
            bucket_id = request.POST['bucket_id']
            if bucket_id==None or bucket_id =="":
                c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'no bucket selected.','trial':trial})
                return render_to_response('explorer/trial_detail.html', c, mimetype="application/xhtml+xml")
            bucket = Bucket.objects.get(pk=bucket_id)
        else: 
            new_bucket_name=request.POST['new_bucket_name']
            if new_bucket_name==None and new_bucket_name =="":
                c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'no new bucket name specified.','trial':trial})
                return render_to_response('explorer/trial_detail.html', c, mimetype="application/xhtml+xml")
            else:
                bucket = Bucket()
                bucket.created_by = request.user
                bucket.title = new_bucket_name
                bucket.save()

        #check if bucket already contains the trial
        assocs = TrialInBucket.objects.filter(Q(trial__id__exact=id) & Q(bin__id__exact=bucket.id))
        if len(assocs) >0:
            c = RequestContext(request, {'title': 'Trial Detail | FeedDB Explorer', 'trial':trial, 'message':'Trial: %s is already in the bucket: %s.' % (trial, bucket)})
            return render_to_response('explorer/trial_detail.html', c, mimetype="application/xhtml+xml")
        #add trials to the bucket
        assoc = TrialInBucket(trial=trial, bin = bucket)
        assoc.save()
        c = RequestContext(request, {'title': 'Trial Detail | FeedDB Explorer', 'trial':trial, 'message':'Trial: %s has been successfully added to the bucket: %s.' % (trial, bucket)})
        return render_to_response('explorer/trial_detail.html', c, mimetype="application/xhtml+xml")

    c = RequestContext(request, {'title': 'Trial Detail | FeedDB Explorer', 'trial':trial, 'message':'not supported action'})
    return render_to_response('explorer/error.html', c, mimetype="application/xhtml+xml")

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



