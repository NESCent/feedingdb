from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import models

def index(request):
    return render_to_response("admin/home.html",{'user':request.user})

def about(request):
    return render_to_response("about.html",{'user':request.user})

def welcome(request):
    return render_to_response("welcome.html",{'user':request.user})