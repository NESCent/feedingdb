from django import template
from django.db.models.loading import get_model
from django.core.exceptions import ImproperlyConfigured
from feeddb.feed.models import Study, Experiment, Session, Trial


register = template.Library()

@register.inclusion_tag('upload_status/upload_status_block.html', takes_context=True)
def upload_status_block(context):
    ret = {}
    ret['known_status'] = True
    try:
        status = context['request'].feed_upload_status
        study = status._data['study']
        ret.update({
            'study': study,
            'subjects': study.subject_set.all(),
            'experiments': study.experiment_set.all(),
            'sessions': Session.objects.filter(study=study),
            'trials': Trial.objects.filter(study=study),
        })
    except (KeyError, AttributeError):
        status = None
        ret['known_status'] = False

    ret['show_status'] = ret['known_status'] and should_show_status(context, status)

    return ret

def should_show_status(context, status):
    try:
        model_name = context['opts'].model_name
        # "original" is the unmodified object, added in ModelAdmin.change_view
        obj = context.get('original', None)
        add = context.get('add', False)

    except KeyError as e:
        raise ImproperlyConfigured('upload_status_block can only be used on admin view, change, or add pages; missing needed context variable: %s' % e)

    Model = get_model('feed', model_name)
    from feeddb.feed.models import CvTerm, FeedBaseModel

    if Model is None:
        return False
    elif issubclass(Model, CvTerm):
        return False
    elif issubclass(Model, FeedBaseModel):
        if add:
            # suppress the block on the Study page
            return Model != Study

        if status is not None and status.object_is_in_study(obj):
            return True

    return False

def get_status(context):
    try:
        status = context['request'].feed_upload_status
    except (KeyError, AttributeError):
        status = None
    return status

@register.inclusion_tag('upload_status/upload_status_current_containers.html', takes_context=True)
def upload_status_current_containers(context):
    # get the data for the upload status block, then remove the
    try:
        model_name = context['opts'].model_name
    except KeyError as e:
        raise ImproperlyConfigured('upload_status_block can only be used on admin view, change, or add pages; missing needed context variable: %s' % e)

    status = get_status(context)
    Model = get_model('feed', model_name)
    ret = {}
    if Model:
        for fname, value in status._data.items():
            if hasattr(Model, fname):
                ret[fname] = value

    ret['status_data'] = status._data
    return ret
