from django.contrib.admin.views.main import ALL_VAR, EMPTY_CHANGELIST_VALUE
from django.contrib.admin.views.main import ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import dateformat
from django.utils.html import escape, conditional_escape
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, AdminFileWidget
from django.conf import settings
from feeddb.feed.models import *
from feeddb.explorer.templatetags.explorer_display import display_file

register = Library()

def _display_readonly_related_field(field, adminform):
    modelname = field.field.field.widget.rel.to._meta.object_name.lower()
    value = adminform.form.initial[field.field.name]
    import collections
    if isinstance(value, collections.Iterable):
        raise ValueError("Not implemented yet")
    else:
        related_obj = field.field.field.to_python(value)
        try:
            url = related_obj.get_absolute_url()
            if url:
                return u'<a href="%s">%s</a>' % (url, related_obj)
        except AttributeError:
            # We handle missing methods as well as empty urls in the same way
            # below.
            pass

        return unicode(related_obj)

@register.inclusion_tag("admin/includes/field.html")
def display_readonly(field, adminform):
    values =[]
    value = field.field.value()

    if value==None:
        value = adminform.form.initial.get(field.field.name)

    if hasattr(value, "append"):
        values =value
    else:
        values.append(value)
    real_value=""
    if value ==None:
        if isinstance(field.field.field.widget, RelatedFieldWidgetWrapper):
            real_value=field.field.field.empty_label
            if real_value!="dead channel":
                real_value=""
    elif isinstance(field.field.field.widget, RelatedFieldWidgetWrapper):
        real_value = _display_readonly_related_field(field, adminform)
    elif hasattr( field.field.field.widget, "choices"):
        for choice in field.field.field.widget.choices:
            for value in values:
                if value == choice[0]:
                    real_value += u'%s<br/>' % choice[1]
    elif isinstance(field.field.field.widget, AdminFileWidget):
        if value!=None and value!="":
            real_value=display_file(value)
    else:
        real_value = value

    return {'value': mark_safe(real_value)}

def display_classname(obj):
    if hasattr(obj, "original"):
        classname = obj.original.__class__.__name__.lower()
    elif hasattr(obj, "formset"):
        classname = obj.formset.model.__name__.lower()
    else:
        classname = obj.__class__.__name__.lower()

    return classname
display_classname = register.simple_tag(display_classname)
