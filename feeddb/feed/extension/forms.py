from django.utils.encoding import smart_unicode, force_unicode
from django.utils.datastructures import SortedDict
from django.utils.text import get_text_list, capfirst
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms.util import ValidationError, ErrorList
from django.forms.forms import BaseForm, get_declared_fields, NON_FIELD_ERRORS
from django.forms.fields import CharField, IntegerField,DecimalField
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

    def __init__(self, *args, **kwargs):
        for key, field in self.base_fields.iteritems():
            if key == "sensor" or key == "channel":
                field.widget = field.hidden_widget()

        super(EmgElectrodeForm, self).__init__(*args, **kwargs)

class EmgSensorForm(forms.ModelForm):
     notes = CharField(widget=HiddenInput(), required=False)
     
     class Meta:
         model = EmgSensor

class SessionForm(forms.ModelForm):
    subj_notes = CharField(label = "Subject Notes", widget=Notes(), required=False)
    class Meta:
        model = Session
        exclude = ('channels',)


class ExperimentForm(forms.ModelForm):
    subject_notes = CharField(label ="Subject Notes", widget=Notes(), required=False)
    description = CharField(label ="Description",widget=Notes(), required=False)
    impl_notes = CharField(label ="Implantation Notes",widget=Notes(), required=False)
    bookkeeping = CharField(label = "Book Keeping", widget=forms.TextInput(attrs={'size': 10}) , required=False)
    accession = CharField(label = "Accession", widget=forms.TextInput(attrs={'size': 10}), required=False)
    subj_tooth = CharField(label = "Subject Tooth", widget=forms.TextInput(attrs={'size': 10}), required=False)
    subj_age = DecimalField(label = "Subject Age", widget=forms.TextInput(attrs={'size': 5}), required=False)
    subj_weight = DecimalField(label = "Subject Weight", widget=forms.TextInput(attrs={'size': 5}), required=False)
    class Meta:
        model = Experiment
        exclude = ('setups',)

class SubjectForm(forms.ModelForm):
    notes = CharField(label ="Subject Notes", widget=Notes(), required=False)
    class Meta:
        model = Subject

class SonoSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = SonoSensor

class SonoChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = SonoChannel

class TrialForm(forms.ModelForm):
    bookkeeping = CharField(label = "Book Keeping", widget=forms.TextInput(attrs={'size': 10}) , required=False)
    accession = CharField(label = "Accession", widget=forms.TextInput(attrs={'size': 5}), required=False)
    position = IntegerField(label = "Position", widget=forms.TextInput(attrs={'size': 3}))
    claimed_duration = DecimalField(label = "Claimed Duration", widget=forms.TextInput(attrs={'size': 5}), required=False)
    subj_notes = CharField(label ="Subject Notes", widget=Notes(), required=False)
    subj_treatment = CharField(label ="Subject Treatment",widget=Notes(), required=False)

    behavior_notes = CharField(label ="Behavior Notes",widget=Notes(), required=False)
    behavior_secondary = CharField(label = "Secondary Behavior", widget=forms.TextInput(attrs={'size': 10}), required=False)
    behavior_notes = CharField(label = "Behavior Notes", widget=Notes(), required=False)

    food_property = CharField(label = "Food Property", widget=forms.TextInput(attrs={'size': 5}), required=False)
    food_size = CharField(label = "Food Size", widget=forms.TextInput(attrs={'size': 5}), required=False)
    food_type = CharField(label = "Food Type", widget=forms.TextInput(attrs={'size': 5}), required=False)

    class Meta:
        model = Trial
        exclude = ('waveform_picture',)

