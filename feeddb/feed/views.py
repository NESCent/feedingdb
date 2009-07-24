from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('template.html', {'content': 'version.html','message':'You have successfully installed the django and set up the the template',})
def view(request,app_name,model_name,object_id):
	return render_to_response('template.html', {'content': 'version.html','message': model_name,})