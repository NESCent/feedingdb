from django import template
from feeddb.feed.models import Techniques

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
    return 0
    return len(formset.formset.initial_forms) + len(formset.formset.extra_forms)
