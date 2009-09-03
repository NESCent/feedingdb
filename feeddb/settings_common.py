import os.path
def relpath2abspath(relpath):
    return os.path.join(os.path.dirname(__file__), relpath).replace('\\','/')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York' 

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = '/Users/vgapeyev/Work/MammFeeding/Django/feeding/feeddb/feed/media'
MEDIA_ROOT = relpath2abspath('feed/media')


TEMPLATE_DIRS = (
   # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
   # Always use forward slashes, even on Windows.
   #"/Users/vgapeyev/Work/MammFeeding/Django/feeding/feeddb/feed/template"
   relpath2abspath('feed/template')
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
   'django.template.loaders.filesystem.load_template_source',
   'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
   'django.middleware.common.CommonMiddleware',
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'feeddb.urls'

INSTALLED_APPS = (
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.sites',
   'django.contrib.admin',
   'feeddb.feed',
)
