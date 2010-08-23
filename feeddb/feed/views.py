from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import models

def index(request):
    return render_to_response("admin/home.html")
