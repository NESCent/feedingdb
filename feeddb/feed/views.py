from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import models

def index(request):
    return HttpResponseRedirect("/admin/")

def view_emgsetup(request, object_id):
    return HttpResponse("viewing emgsetup")
    
def edit_emgsetup(request, object_id):
    return HttpResponse("editing emgsetup")
