from django.utils.encoding import smart_unicode, force_unicode
from django.utils.datastructures import SortedDict
from django.utils.text import get_text_list, capfirst
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms.util import ValidationError, ErrorList
from django.forms.forms import BaseForm, get_declared_fields, NON_FIELD_ERRORS
from django.forms.fields import *
from django.forms.widgets import Select, SelectMultiple, HiddenInput, MultipleHiddenInput, DateInput, RadioSelect
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
                self.base_fields[f].widget.attrs['readonly']=""
        super(DisableForeignKeyForm, self).__init__(*args, **kwargs)

#exclude technique from all types of setups
class SetupForm (DisableForeignKeyForm):
    class Meta:
        exclude = ('technique',)

class ExperimentChangeForm(DisableForeignKeyForm):
    setup_types = MultipleChoiceField(label="Sensor Types", choices=TECHNIQUE_CHOICES_NAMED, required=False)

    class Meta:
        widgets = {
            'start': DateInput(attrs={'class':'datepicker'}),
            'end': DateInput(attrs={'class':'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial')
        if instance is not None:
            if initial is None:
                initial = {}

            setup_types = []
            for name, label in TECHNIQUE_CHOICES_NAMED:
                if instance.has_setup_type(name):
                    setup_types.append(name)

            initial['setup_types'] = setup_types
            kwargs['initial'] = initial
        return super(ExperimentChangeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        """
        When saving the form, expand `setup_types` into a list of setups to
        save, then duplicate the standard behavior from superclass.
        """
        from django.db.models.loading import get_model

        experiment = super(ExperimentChangeForm, self).save(commit=False, *args, **kwargs)
        setup_types = self.cleaned_data.get('setup_types', None)
        self._setups_to_save = []
        for setup_name in setup_types:
            if not experiment.has_setup_type(setup_name):
                TypedSetup = get_model('feed', setup_name)
                setup = TypedSetup()
                setup.experiment = experiment
                setup.technique = Techniques.name2num(setup_name)
                # FIXME: should use request.user if available
                setup.created_by = experiment.created_by
                self._setups_to_save.append(setup)

        save_m2m = self.save_m2m
        def new_save_m2m():
            save_m2m()
            for setup in self._setups_to_save:
                # This line avoids an IntegrityError in setup.save(). Insanity.
                setup.experiment = setup.experiment
                setup.save()

        if commit:
            experiment.save()
            new_save_m2m()
        else:
            self.save_m2m = new_save_m2m

        return experiment

class StudyChangeForm(forms.ModelForm):
    #start = DateTimeField("Start Date", help_text=DATE_HELP_TEXT)
    #end = DateTimeField("ENDZ", required=False, help_text=DATE_HELP_TEXT)
    #approval_type = forms.ModelChoiceField(
    #    queryset=AnimalApprovalType.objects.all(),
    #    widget=RadioSelect(),
    #    empty_label="No approval secured",
    #    label="Approval Secured",
    #    help_text
    #)
    class Meta:
        model=Study
        widgets = {
            'start': DateInput(attrs={'class':'datepicker'}),
            'end': DateInput(attrs={'class':'datepicker'}),
            'approval_type': RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(StudyChangeForm, self).__init__(*args, **kwargs)
        self.fields['approval_type'].empty_label = 'No approval'

class SessionChangeForm(forms.ModelForm):
    class Meta:
        widgets = {
            'start': DateInput(attrs={'class':'datepicker'}),
            'end': DateInput(attrs={'class':'datepicker'}),
        }

class TrialChangeForm(forms.ModelForm):
    class Meta:
        widgets = {
            'start': DateInput(attrs={'class':'datepicker'}),
            'end': DateInput(attrs={'class':'datepicker'}),
        }

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
        exclude = ('channels',)

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
        exclude = ('setups',)

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

class OtherChannelForm(forms.ModelForm):
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)
    class Meta:
        model = OtherChannel

class TrialInlineForm(forms.ModelForm):
    bookkeeping = CharField(label = "Book Keeping", widget=forms.TextInput(attrs={'size': 10}) , required=False)
    position = IntegerField(label = "Position", widget=forms.TextInput(attrs={'size': 3}))
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

class ChannelLineupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['channel'].empty_label='dead channel'
        super(ChannelLineupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ChannelLineup



