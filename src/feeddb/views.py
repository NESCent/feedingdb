# VG: I suggest this usage for views.py: 
#  This is where back end (DB access & data massaging) and 
#  front end (presentation on web pages) are connected to each other. 
#  We will only keep the connecting code here. 
#  All non-trivial computations should be factored out separate modules. 

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, Template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.conf import settings

def logout_view(request):
    logout(request)
    message = 'You have logged out.'
    c = RequestContext(request, {'title': 'FeedDB', 'message': message})
    next = '/'
    return HttpResponseRedirect(next)

def login_view(request):
    if request.user.is_authenticated() and request.user.first_name!="anonymous":
        return HttpResponseRedirect('/welcome')
    message = 'Please login'
    if request.method == 'GET':
        next = '/welcome'
        if request.GET.has_key('next'):
            next = request.GET['next'] 
        c = RequestContext(request, {'title': 'FeedDB', 'message': message, 'next':next})
        return render_to_response('admin/login.html', c)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = '/welcome'
                if request.POST.has_key('next'):
                    next = request.POST['next'] 
                #VG: I think the following 'if' is unreachable code  2011-02-01
                if not next is None and next !="": 
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect("/")
            else:
                message = "This account is deactivated." 
        else:
            message = "No matched account found. Please try again."

        next = '/welcome'
        if request.GET.has_key('next'):
            next = request.GET['next'] 
        c = RequestContext(request, {'title': 'FeedDB', 'message': message, 'next':next })
        return render_to_response('admin/login.html', c)

