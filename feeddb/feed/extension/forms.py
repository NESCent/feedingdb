from django.utils.encoding import smart_unicode, force_unicode
from django.utils.datastructures import SortedDict
from django.utils.text import get_text_list, capfirst
from django.utils.translation import ugettext_lazy as _, ugettext

from django.forms.util import ValidationError, ErrorList
from django.forms.forms import BaseForm, get_declared_fields, NON_FIELD_ERRORS
from django.forms.fields import CharField, IntegerField
from django.forms.widgets import Select, SelectMultiple, HiddenInput, MultipleHiddenInput
from django.forms.widgets import media_property
from django.forms.formsets import BaseFormSet, formset_factory, DELETION_FIELD_NAME
from django import forms
from feeddb.feed.models import *
from feeddb.feed.extension.widgets import *

class EmgElectrodeForm(forms.ModelForm):
     notes = CharField(label="Notes", widget=Notes(), required=False)
     name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}))

     class Meta:
         model = EmgElectrode


class EmgSensorForm(forms.ModelForm):
     notes = CharField(widget=HiddenInput(), required=False)
     
     class Meta:
         model = EmgSensor

class SessionForm(forms.ModelForm):
    subj_notes = CharField(widget=Notes(), required=False)
    class Meta:
        model = Session
        exclude = ('channels',)
