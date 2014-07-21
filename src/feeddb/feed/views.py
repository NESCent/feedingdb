from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import models

def index(request):
    return render(request, "admin/home.html",{'user':request.user})

def about(request):
    return render(request, "about.html",{'user':request.user})

def welcome(request):
    return render(request, "welcome.html",{'user':request.user})
