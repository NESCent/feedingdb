from django.template import Library

register = Library()

def app_static_prefix():
    """
    Returns the string contained in the setting settings.STATIC_URL.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.STATIC_PREFIX
app_static_prefix = register.simple_tag(app_static_prefix)
