from django.conf import settings
from django.contrib.admin.views.main import ALL_VAR, EMPTY_CHANGELIST_VALUE
from django.contrib.admin.views.main import ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import dateformat
from django.utils.html import escape, conditional_escape
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.utils.translation import get_date_formats, get_partial_date_formats, ugettext as _
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist

register = Library()

def display_readonly(field, adminform):
    
    values =[]
    value = adminform.form.initial.get(field.field.name)
    real_value=""
    if field.field.field.widget.__class__.__name__ == "RelatedFieldWidgetWrapper":
        
        if hasattr(value, "append"):
            values =value
        else:
            values.append(value)
        for choice in field.field.field.widget.widget.choices:
            modelname = field.field.field.widget.rel.to._meta.object_name.lower()
            for value in values:
                if value == choice[0]:
                    if modelname  != "group" and modelname  != "permission":
                        real_value += u'<a href="/admin/%s/%s/%s">%s</a><br/>' % ("feed", field.field.field.widget.rel.to._meta.object_name.lower(), value, choice[1])
                    else:
                        real_value += u'%s<br/>' % choice[1]
    else:
        real_value = value
         
    return {'value': mark_safe(real_value)}
display_readonly = register.inclusion_tag("admin/includes/field.html")(display_readonly)


