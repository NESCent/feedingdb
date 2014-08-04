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


# URL prefix for admin static files -- CSS, JavaScript and images. 
# Make sure to use a trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# FEED: In development, Admin serves this URL magically from site-packages. 
#          In deployment, Apache must be configured to serve them directly. 
ADMIN_MEDIA_PREFIX = '/adminstatic/' 

# FEED: STATIC_XXX are home-grown variables. 
# They point to the store for static files (CSS, JS, images) of feeddb.feed app.
STATIC_ROOT = relpath2abspath('feed/static')
STATIC_PREFIX='/static/'
STATIC_URL=STATIC_PREFIX

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# FEED: We use MEDIA_XXX only to store & server the user-uploaded files. 
#   The MEDIA_ROOT var should be defined in the local settings.py
MEDIA_URL = '/uploads/'

# Absolute path to [project root]/explorer/static, which holds
# web-related files of the explorer app, like css stylesheets or images. 
EXPLORER_STATIC_ROOT = relpath2abspath('explorer/static')


TEMPLATE_DIRS = (
   # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
   # Always use forward slashes, even on Windows.
   #"/Users/vgapeyev/Work/MammFeeding/Django/feeding/feeddb/feed/template"
   relpath2abspath('feed/templates'),
   relpath2abspath('explorer/templates')
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

MIDDLEWARE_CLASSES = (
   'django.middleware.common.CommonMiddleware',
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'debug_toolbar.middleware.DebugToolbarMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',
   'feeddb.feed.extension.middleware.AnonymousAccessMiddleware',
   'pagination.middleware.PaginationMiddleware',
   
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'feeddb.urls'

INSTALLED_APPS = (
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.sites',
   'django.contrib.admin',
   'django.contrib.staticfiles',
   'south',
   'feeddb.feed',
   'feeddb.explorer',
   'pagination',
   'haystack',
   'debug_toolbar',
   #'inspector_panel',
   'feeddb.faceted_search',
)

### Debug toolbar configuration
def custom_toolbar_show(request):
    return 'show_debug_toolbar' in request.session and request.session['show_debug_toolbar']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'feeddb.settings.custom_toolbar_show',
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False

#DEBUG_TOOLBAR_PANELS = (
#    #'inspector_panel.panels.inspector.InspectorPanel',
#)
