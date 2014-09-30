from django import template
from django.db.models.loading import get_model
from django.core.exceptions import ImproperlyConfigured

register = template.Library()

@register.inclusion_tag('upload_status/upload_status_block.html', takes_context=True)
def upload_status_block(context):
    ret = {}
    ret['known_status'] = True
    try:
        status = context['request'].feed_upload_status
        ret.update(status.get_dict())
    except (KeyError, AttributeError):
        status = None
        ret['known_status'] = False

    ret['show_status'] = ret['known_status'] and should_show_status(context, status)

    return ret

def should_show_status(context, status):
    try:
        model_name = context['opts'].model_name
        # "original" is the unmodified object, added in ModelAdmin.change_view
        obj = context['original']
        add = context.get('add', False)

    except KeyError as e:
        raise ImproperlyConfigured('upload_status_block can only be used on admin forms; missing needed context variable: %s' % e)

    Model = get_model('feed', model_name)


    from feeddb.feed.models import CvTerm, FeedBaseModel

    if issubclass(Model, CvTerm):
        return False
    elif issubclass(Model, FeedBaseModel):
        if add:
            return True

        if status is not None and status.object_is_in_study(context['original']):
            return True

    return False
