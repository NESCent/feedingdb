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
    return len(formset.formset.initial_forms) + len(formset.formset.extra_forms)

@register.simple_tag
def add_new_to_container_url(regrouped):
    try:
        container = regrouped['grouper']
        containertypename = type(container).__name__.lower()
        subtypename = type(regrouped['list'].pop().original).__name__.lower()
        return reverse('admin:feed_%s_add' % subtypename) + '?%s=%d' % (containertypename, container.id)
    except KeyError:
        raise ImproperlyConfigured('add_new_to_container_url requires as an argument a "regrouped" item container')
