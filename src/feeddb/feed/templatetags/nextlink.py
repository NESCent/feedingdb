from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def querystring_url(context, qs_key, default=False):
    '''
    Get an absolute URL by interpreting the value from the querystring. Returns
    False if the value could not be found.
    '''
    try:
        request = context['request']
        given_url = request.GET[qs_key]
        return request.build_absolute_uri(given_url)
    except (AttributeError, KeyError):
        if default and isinstance(default, basestring):
            return request.build_absolute_uri(default)
        else:
            return ''

@register.simple_tag(takes_context=True)
def cancel_url(context):
    return querystring_url(context, 'cancel', default='../')

@register.simple_tag(takes_context=True)
def next_url(context):
    '''
    Returns empty string if cannot be found
    '''
    return  querystring_url(context, 'next')

