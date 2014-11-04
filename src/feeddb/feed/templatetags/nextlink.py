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
    return querystring_url(context, 'next')

@register.simple_tag(takes_context=True)
def next_or_study_url(context):
    """
    Returns the value of next_url() or, if undefined, the current study URL if
    known.
    """
    try:
        import upload_status
        containers = upload_status.get_current_containers(context)
        study_url = containers['study'].get_absolute_url()
    except:
        study_url = False

    return querystring_url(context, 'next', default=study_url)
