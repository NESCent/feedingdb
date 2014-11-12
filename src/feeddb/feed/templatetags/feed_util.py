from django import template
from feeddb.feed.models import Techniques
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

register = template.Library()

@register.inclusion_tag('model_help_text.html')
def model_help_text(obj):
    try:
        return obj.FeedMeta.__dict__
    except AttributeError:
        return {}

@register.filter
def technique_name(val):
    return Techniques.num2label(val)

@register.filter
def formset_length(formset):
    return len(formset.formset.initial_forms)

subtypenames = {
    'experiment': 'session',
    'session': 'trial',
}

@register.simple_tag
def add_new_to_container_url(regrouped):
    try:
        container = regrouped['grouper']
        containertypename = type(container).__name__.lower()
        try:
            subtypename = subtypenames[containertypename]
        except KeyError:
            raise ValueError('Container type "%s" is not supported.' % containertypename)

        return reverse('admin:feed_%s_add' % subtypename) + '?%s=%d' % (containertypename, container.id)
    except KeyError:
        raise ImproperlyConfigured('add_new_to_container_url requires as an argument a "regrouped" item container')

@register.simple_tag
def delete_object_and_redirect_to_study_url(original):
    typename = type(original).__name__.lower()
    delete_url = reverse('admin:feed_%s_delete' % typename, args=(original.pk,))
    try:
        study = original.study
        delete_url += '?%s=%d' % ('study', study.pk)
    except AttributeError:
        pass

    return delete_url
