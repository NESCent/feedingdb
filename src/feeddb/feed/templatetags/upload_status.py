from django import template

register = template.Library()

@register.inclusion_tag('upload_status/upload_status_block.html', takes_context=True)
def upload_status_block(context):
    ret = { 'known_status': True } 
    try:
        ret.update(context['request'].feed_upload_status.get_dict())
    except (KeyError, AttributeError):
        ret['known_status'] = False

    return ret
