from django.utils.encoding import smart_unicode, force_unicode
from django.utils.datastructures import SortedDict
from django.utils.text import get_text_list, capfirst
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms.util import ValidationError, ErrorList
from django.forms.forms import BaseForm, get_declared_fields, NON_FIELD_ERRORS
from django.forms.fields import *
from django.forms.widgets import Select, SelectMultiple, HiddenInput, MultipleHiddenInput
from django.forms.widgets import media_property
from django.forms.formsets import BaseFormSet, formset_factory, DELETION_FIELD_NAME
from django import forms
from feeddb.feed.models import *
from feeddb.feed.extension.widgets import *
from feeddb.feed.extension.fields import FeedDateTimeField

from django.db import models

DATE_HELP_TEXT = 'format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00'
class ExperimentChangeForm(forms.ModelForm):
    start = FeedDateTimeField(required=False, help_text=DATE_HELP_TEXT)
    end = FeedDateTimeField(required=False, help_text=DATE_HELP_TEXT)
    def __init__(self, *args, **kwargs):
        parent_obj =None
        obj = None
        
        if 'initial' in kwargs:
            if 'study' in kwargs['initial']:
                study_id=kwargs['initial']['study']
                parent_obj = Study.objects.get(id=study_id)
                for key, field in self.base_fields.iteritems():
                    if key =="start":
                        field.initial=parent_obj.start 
                    if key =="end":
                        field.initial=parent_obj.end
                         
        super(ExperimentChangeForm, self).__init__(*args, **kwargs)

class StudyChangeForm(forms.ModelForm):
    start = FeedDateTimeField(help_text=DATE_HELP_TEXT)
    end = FeedDateTimeField(required=False,help_text=DATE_HELP_TEXT)

class SessionChangeForm(forms.ModelForm):
    start = FeedDateTimeField(required=False, help_text=DATE_HELP_TEXT)
    end = FeedDateTimeField(required=False, help_text=DATE_HELP_TEXT)
    def __init__(self, *args, **kwargs):
        parent_obj =None
        obj = None
        if 'initial' in kwargs:
            if 'experiment' in kwargs['initial']:
                experiment_id=kwargs['initial']['experiment']
                parent_obj = Experiment.objects.get(id=experiment_id)
                for key, field in self.base_fields.iteritems():
                    if key =="start":
                        field.initial=parent_obj.start 
                    if key =="end":
                        field.initial=parent_obj.end
                         
        super(SessionChangeForm, self).__init__(*args, **kwargs)

class TrialChangeForm(forms.ModelForm):
    start = FeedDateTimeField(required=False, help_text=DATE_HELP_TEXT)
    end = FeedDateTimeField(required=False, help_text=DATE_HELP_TEXT)
    def __init__(self, *args, **kwargs):
        parent_obj =None
        obj = None
        
        if 'initial' in kwargs:
            if 'session' in kwargs['initial']:
                session_id=kwargs['initial']['session']
                parent_obj = Session.objects.get(id=session_id)
                for key, field in self.base_fields.iteritems():
                    if key =="start":
                        field.initial=parent_obj.start 
                    if key =="end":
                        field.initial=parent_obj.end
                         
        super(TrialChangeForm, self).__init__(*args, **kwargs)

class EmgChannelForm(forms.ModelForm):
    class Meta:
        model = EmgChannel

    def __init__(self, *args, **kwargs):
        for key, field in self.base_fields.iteritems():
            if key == "setup" or key == "name" or key == "notes":
                field.widget = field.hidden_widget()
            if key =="name":
                field.initial="EMG Channel"    

        super(EmgChannelForm, self).__init__(*args, **kwargs)
        
class EmgSensorChannelForm(forms.ModelForm):
    rate = forms.IntegerField(label = "Recording Rate (Hz)", required=True, widget=forms.TextInput(attrs={'size': 5}))
    emg_unit = forms.ModelChoiceField(label = "Emg Unit", required=True,queryset=Emgunit.objects.all())
    emg_filtering = forms.ModelChoiceField(label="EMG filtering", queryset=Emgfiltering.objects.all())
    emg_amplification = IntegerField(label = "Amplification",required=False, initial='', widget=forms.TextInput(attrs={'size': 5}))
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}))

    class Meta:
        model = EmgSensor
        fields = ['setup','name', 'location_controlled', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'axisdepth', 'notes']

    def __init__(self, *args, **kwargs):
        channel=None
        if 'instance' in kwargs:
            sensor=kwargs['instance']
            try:
                channel = EmgChannel.objects.get(sensor__id__exact = sensor.id)
            except EmgChannel.DoesNotExist:
                channel = None
        if channel !=None:    
            self.base_fields["emg_unit"].initial = channel.emg_unit.id
            for key, field in self.base_fields.iteritems():
                if key =="emg_amplification":
                    field.initial=channel.emg_amplification
#                if key =="emg_unit":
#                    field.initial= channel.emg_unit.id
                if key =="emg_filtering":
                    field.initial=channel.emg_filtering.id  
                if key =="rate":
                    field.initial=channel.rate            
        else:
            self.base_fields["emg_unit"].initial = None
            for key, field in self.base_fields.iteritems():
                if key =="emg_amplification":
                    field.initial=None
#                if key =="emg_unit":
#                    field.initial= None
                if key =="emg_filtering":
                    field.initial=None   
                if key =="rate":
                    field.initial=None            
        
        super(EmgSensorChannelForm, self).__init__(*args, **kwargs)
    
class EmgSensorForm(EmgSensorChannelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    ordering='name'
         
class SessionForm(forms.ModelForm):
    subj_notes = CharField(label = "Subject Notes", widget=Notes(attrs={'size': 5}), required=False)
    accession = CharField(label = "Accession", widget=forms.TextInput(attrs={'size': 5}), required=False)
    bookkeeping = CharField(label = "Book Keeping", widget=forms.TextInput(attrs={'size': 10}) , required=False)
    position = IntegerField(label = "Position", help_text='the order of the recording session in the experiment', widget=forms.TextInput(attrs={'size': 3}))
    start = FeedDateTimeField(required=False)
    end = FeedDateTimeField(required=False)
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
        fields = ['name', 'location_controlled', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'axisdepth', 'notes']

class SonoChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = SonoChannel

class StrainSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = StrainSensor
        fields = ['name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes']
        
class StrainChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = StrainChannel

class ForceSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = ForceSensor
        fields = ['name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes']
                
class ForceChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = ForceChannel
class PressureSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = PressureSensor
        fields = ['name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes']
                
class PressureChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = PressureChannel        

class KinematicsSensorForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = KinematicsSensor
        fields = ['name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes']
                
class KinematicsChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=Notes(), required=False)
    class Meta:
        model = KinematicsChannel    
                
class TrialInlineForm(forms.ModelForm):
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

class TrialForm(forms.ModelForm):
    #remove_waveform_picture = forms.BooleanField(required=False)
    #def save(self, *args, **kwargs):
    #    object = super(TrialForm, self).save(*args, **kwargs)
    #    if self.cleaned_data.get('remove_waveform_picture'):
    #        object.waveform_picture = ''
    #    return object
    
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for key, field in self.base_fields.iteritems():
            if(key =="data_file"):
                field.widget = field.hidden_widget()
                field.help_text ="Please upload data file after saving the new trial."
        

    class Meta:
        model = Trial

class ChannelLineupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        for key, field in self.base_fields.iteritems():
            if(key =="channel"):
                field.empty_label = 'dead channel'
        super(ChannelLineupForm, self).__init__(*args, **kwargs)
                
    class Meta:
        model = ChannelLineup       