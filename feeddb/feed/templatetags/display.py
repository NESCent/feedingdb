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
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, AdminFileWidget
from django.conf import settings
from feeddb.feed.models import *
from feeddb.explorer.templatetags.explorer_display import display_file

register = Library()

def display_readonly(field, adminform):
    values =[]
    value=field.field.field.initial
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
    elif isinstance(field.field.field.widget, RelatedFieldWidgetWrapper):
        for choice in field.field.field.widget.widget.choices:
            modelname = field.field.field.widget.rel.to._meta.object_name.lower()

            if modelname=="setup":
                if isinstance(adminform.form.instance, EmgSensor) or isinstance(adminform.form.instance, EmgChannel):
                    modelname ="emgsetup"
                elif isinstance(adminform.form.instance, SonoSensor) or isinstance(adminform.form.instance, SonoChannel):
                    modelname ="sonosetup"
                elif isinstance(adminform.form.instance, StrainSensor) or isinstance(adminform.form.instance, StrainChannel):
                    modelname ="strainsetup"
                elif isinstance(adminform.form.instance, PressureSensor) or isinstance(adminform.form.instance, PressureChannel):
                    modelname ="pressuresetup"
                elif isinstance(adminform.form.instance, ForceSensor) or isinstance(adminform.form.instance, ForceChannel):
                    modelname ="forcesetup"
                elif isinstance(adminform.form.instance, KinematicsSensor) or isinstance(adminform.form.instance,KinematicsChannel):
                    modelname ="kinematicssetup"            
                else:
                    modelname=""    
            for value in values:
                if value == choice[0]:
                    if modelname!="" and modelname  != "group" and modelname  != "permission":
                        real_value += u'<a href="/admin/%s/%s/%s">%s</a><br/>' % ("feed", modelname, value, choice[1])
                    else:
                        real_value += u'%s<br/>' % choice[1]
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
display_readonly = register.inclusion_tag("admin/includes/field.html")(display_readonly)


def display_classname(obj):
    if hasattr(obj, "original"):
        classname = obj.original.__class__.__name__.lower()
    elif hasattr(obj, "formset"):
        classname = obj.formset.model.__name__.lower()
    else:
        classname = obj.__class__.__name__.lower()
    
    return classname
display_classname = register.simple_tag(display_classname)
