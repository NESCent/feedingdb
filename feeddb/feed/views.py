from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def index(request):
    return HttpResponseRedirect("/admin/")