from django.template import Library

register = Library()

def app_static_prefix():
    """
    Returns the string contained in the setting STATIC_MEDIA_PREFIX.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_URL
app_static_prefix = register.simple_tag(app_static_prefix)
