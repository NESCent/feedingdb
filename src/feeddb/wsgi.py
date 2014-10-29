"""
WSGI config for feeddb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys

# Allow Django to find the `feeddb` module by appending the parent directory to
# the PATH variable
base = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feeddb.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
 