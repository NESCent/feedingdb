from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User

#
# middleware class to automatically login anonymous user if  ALLOW_ANONYMOUS_ACCESS is True in settings.py file
#

class AnonymousAccessMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated() and settings.ALLOW_ANONYMOUS_ACCESS:
            username = settings.ANONYMOUS_USERNAME
            password = settings.ANONYMOUS_PASSWORD
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)