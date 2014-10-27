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
        obj = context.get('original', context.get('object', None))
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

def get_current_containers(context):
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

    ret['model_name'] =  model_name
    ret['Model'] = Model
    ret['status'] = status
    ret['status_data'] = status._data
    return ret

@register.inclusion_tag('upload_status/upload_status_current_containers.html', takes_context=True)
def upload_status_current_containers(context):
    return get_current_containers(context)

@register.simple_tag(takes_context=True)
def upload_status_model_add_url(context, inline, **kwargs):
    "`inline` is usually inline_admin_formset.opts, which is, e.g. SubjectViewInline"
    modelname = inline.model.__name__.lower()
    request = context['request']
    return request.feed_upload_status.model_add_url(modelname, **kwargs)

@register.simple_tag(takes_context=True)
def setup_or_add_session_text(context):
    request = context['request']
    status = request.feed_upload_status
    obj = context.get('original', context.get('object', None))
    if obj:
        next_url = status.next_setup_or_session_url(request, {}, obj)
        session_url = status.contextualized_model_add_url('session', request, {}, obj)
        if next_url == session_url:
            return 'Save &amp; Add Session'
        else:
            return 'Save &amp; Edit Sensors'
