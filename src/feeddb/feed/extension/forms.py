from django.utils.encoding import smart_unicode, force_unicode
from django.utils.datastructures import SortedDict
from django.utils.text import get_text_list, capfirst
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms.util import ValidationError, ErrorList
from django.forms.forms import BaseForm, get_declared_fields, NON_FIELD_ERRORS
from django.forms.fields import *
from django.forms.widgets import Select, SelectMultiple, HiddenInput, MultipleHiddenInput, SplitDateTimeWidget
from django.forms.widgets import media_property
from django.forms.formsets import BaseFormSet, formset_factory, DELETION_FIELD_NAME
from django import forms
from feeddb.feed.models import *
from feeddb.feed.extension.widgets import *

from django.db import models


# Monkey-patch widgets.Select.render() to add the "chosen" class always
oldRender = Select.render
def newRender(self, *args, **kwargs):
    self.attrs['class'] = 'chosen-select' + self.attrs.get('class', '')
    return oldRender(self, *args, **kwargs)
Select.render = newRender

DATE_HELP_TEXT = DATETIME_HELP_TEXT  #imported from feeddb.feed.models
DISABLE_FIELDS = ['study','experiment','session','setup']

#use this form as the super class for hiding foreign keys in editing form
class DisableForeignKeyForm (forms.ModelForm):
    def __init__(self, *args, **kwargs):
        for f in DISABLE_FIELDS:
            if f in self.base_fields:
                self.base_fields[f].widget.attrs['disabled']=""
        super(DisableForeignKeyForm, self).__init__(*args, **kwargs)    

#exclude technique from all types of setups                 
class SetupForm (DisableForeignKeyForm):
    class Meta:
        exclude = ('technique',)


class ExperimentChangeForm(DisableForeignKeyForm):
    start = DateField(required=False, help_text=DATE_HELP_TEXT)
    end = DateField(required=False, help_text=DATE_HELP_TEXT)

class StudyChangeForm(forms.ModelForm):
    #start = DateTimeField("Start Date", help_text=DATE_HELP_TEXT)
    #end = DateTimeField("ENDZ", required=False, help_text=DATE_HELP_TEXT)
    class Meta:
        model=Study
        widgets = {
            'start': SplitDateTimeWidget(attrs={'class':'datepicker'}),
            'end': SplitDateTimeWidget(attrs={'class':'datepicker'}),
        }

class SessionChangeForm(forms.ModelForm):
    start = DateField(required=False, help_text=DATE_HELP_TEXT)
    end = DateField(required=False, help_text=DATE_HELP_TEXT)

class TrialChangeForm(forms.ModelForm):
    start = DateField(required=False)  # , help_text=DATE_HELP_TEXT)
    end = DateField(required=False)    # , help_text=DATE_HELP_TEXT)
# Compared to the other containers above, Trial help_text is affected by models.py -- go figure why (VG)

class EmgSensorChannelForm(forms.ModelForm):
    rate = forms.IntegerField(label = "Recording Rate (Hz)", required=True, widget=forms.TextInput(attrs={'size': 5}))
    unit = forms.ModelChoiceField(label = "Emg Units", required=True,queryset=Unit.objects.filter(technique = Techniques.ENUM.emg))
    emg_filtering = forms.ModelChoiceField(label="EMG filtering", queryset=Emgfiltering.objects.all())
    emg_amplification = IntegerField(label = "Amplification",required=False, initial='', widget=forms.TextInput(attrs={'size': 5}))
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}))
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    muscle = forms.ModelChoiceField(label="Muscle", required=False, queryset=MuscleOwl.default_qs())

    def __init__(self, *args, **kwargs):
        channel=None
        if 'instance' in kwargs:
            sensor=kwargs['instance']
            try:
                channel = EmgChannel.objects.get(sensor__id__exact = sensor.id)
            except EmgChannel.DoesNotExist:
                channel = None
        if channel !=None:    
            self.base_fields["unit"].initial = channel.unit.id 
            self.base_fields["emg_amplification"].initial = channel.emg_amplification
            self.base_fields["emg_filtering"].initial = channel.emg_filtering.id
            self.base_fields["rate"].initial = channel.rate
        else:
            self.base_fields["unit"].initial = None
            self.base_fields["emg_amplification"].initial = None
            self.base_fields["emg_filtering"].initial = None
            self.base_fields["rate"].initial = None
        super(EmgSensorChannelForm, self).__init__(*args, **kwargs)

class SessionForm(forms.ModelForm):
    subj_notes = CharField(label = "Subject Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    bookkeeping = CharField(label = "Book Keeping", widget=forms.TextInput(attrs={'size': 10}) , required=False)
    position = IntegerField(label = "Position", help_text='the order of the recording session in the experiment', widget=forms.TextInput(attrs={'size': 3}))
    start = DateTimeField(required=False)
    end = DateTimeField(required=False)
    class Meta:
        model = Session
        exclude = ('channels','accession')
        
class ExperimentForm(forms.ModelForm):
    subject_notes = CharField(label ="Subject Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    description = CharField(label ="Description",widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    impl_notes = CharField(label ="Implantation Notes",widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    bookkeeping = CharField(label = "Book Keeping", widget=forms.TextInput(attrs={'size': 10}) , required=False)
    subj_tooth = CharField(label = "Subject Tooth", widget=forms.TextInput(attrs={'size': 10}), required=False)
    subj_age = DecimalField(label = "Subject Age", widget=forms.TextInput(attrs={'size': 5}), required=False)
    #VG 2010-10-29 not sure correct field type for ageunit, but it appears dead code, anyway
    subj_ageunit = CharField(label = "Age Units", widget=forms.TextInput(attrs={'size': 10}), required=False)
    subj_weight = DecimalField(label = "Subject Weight (Kg)", widget=forms.TextInput(attrs={'size': 5}), required=False)
    title = CharField(label = "Title", widget=forms.TextInput(attrs={'size': 10}))
    class Meta:
        model = Experiment
        exclude = ('setups','accession')

class SubjectForm(forms.ModelForm):
    notes = CharField(label ="Subject Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    class Meta:
        model = Subject

class SonoSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    muscle = forms.ModelChoiceField(label="Muscle", required=False, queryset=MuscleOwl.default_qs())
    
    class Meta:
        model = SonoSensor
        fields = ['name', 'location_controlled', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'axisdepth', 'notes']

class SonoChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    class Meta:
        model = SonoChannel

class StrainSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    location_freetext = CharField(label = "Location", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    
    class Meta:
        model = StrainSensor
        fields = ['name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes']
        
class StrainChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    class Meta:
        model = StrainChannel

class ForceSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    location_freetext = CharField(label = "Location", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    class Meta:
        model = ForceSensor
        fields = ['name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes']
                
class ForceChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    class Meta:
        model = ForceChannel
class PressureSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    location_freetext = CharField(label = "Location", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    class Meta:
        model = PressureSensor
        fields = ['name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes']
                
class PressureChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    class Meta:
        model = PressureChannel        

class KinematicsSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    location_freetext = CharField(label = "Location", widget=forms.TextInput(attrs={'size': 10}) , required=True)
    class Meta:
        model = KinematicsSensor
        fields = ['name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes']
                
class KinematicsChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    class Meta:
        model = KinematicsChannel    
        
class EventChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    class Meta:
        model = EventChannel        
    
    
                
class TrialInlineForm(forms.ModelForm):
    bookkeeping = CharField(label = "Book Keeping", widget=forms.TextInput(attrs={'size': 10}) , required=False)
    position = IntegerField(label = "Position", widget=forms.TextInput(attrs={'size': 3}))
    estimated_duration = IntegerField(label = "Estimated Duration (sec)", widget=forms.TextInput(attrs={'size': 10}), required=False)
    subj_notes = CharField(label ="Subject Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    subj_treatment = CharField(label ="Subject Treatment",widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)

    behavior_notes = CharField(label ="Behavior Notes",widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    behavior_secondary = CharField(label = "Secondary Behavior", widget=forms.TextInput(attrs={'size': 10}), required=False)
    behavior_notes = CharField(label = "Behavior Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)

    food_property = CharField(label = "Food Property", widget=forms.TextInput(attrs={'size': 5}), required=False)
    food_size = CharField(label = "Food Size(maximum dimension millimeters)", widget=forms.TextInput(attrs={'size': 5}), required=False)
    food_type = CharField(label = "Food Type", widget=forms.TextInput(attrs={'size': 5}), required=False)

    class Meta:
        model = Trial
        exclude = ( 'accession', )

class TrialForm(forms.ModelForm):
    #remove_waveform_picture = forms.BooleanField(required=False)
    #def save(self, *args, **kwargs):
    #    object = super(TrialForm, self).save(*args, **kwargs)
    #    if self.cleaned_data.get('remove_waveform_picture'):
    #        object.waveform_picture = ''
    #    return object
    
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.base_fields['data_file'].widget = self.base_fields['data_file'].hidden_widget()
        self.base_fields['data_file'].help_text ="Please upload data file after saving the new trial."
        
    class Meta:
        model = Trial

class ChannelLineupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['channel'].empty_label='dead channel'
        super(ChannelLineupForm, self).__init__(*args, **kwargs)
                
    class Meta:
        model = ChannelLineup       


       
