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

def validate_start_end(cleaned_data):
    """
    Helper method used in Form.clean() methods to check start and end date
    sanity
    """
    start = cleaned_data['start']
    end = cleaned_data['end']
    if end is not None and end < start:
        raise ValidationError('Problem with start and end dates: end must post-date start')

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
    setup_types = MultipleChoiceField(label="Sensor Types", choices=TECHNIQUE_CHOICES_NAMED, required=True, help_text="Add setups by selecting sensor types here. To delete a setup, visit the experiment's view page and click on the setup's tab." )

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

    def clean(self):
        cleaned_data = super(ExperimentChangeForm, self).clean()
        validate_start_end(cleaned_data)
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        """
        When saving the form, expand `setup_types` into a list of setups to
        save, then duplicate the standard behavior from superclass.
        """
        from django.db.models.loading import get_model

        experiment = super(ExperimentChangeForm, self).save(commit=False, *args, **kwargs)
        new_setup_types = self.cleaned_data.get('setup_types', None)
        self._setups_to_save = []
        old_setup_types = experiment.get_setup_types(freshen=True)
        added_setup_types = set(new_setup_types) - set(old_setup_types)
        deleted_setup_types = set(old_setup_types) - set(new_setup_types)
        for setup_name in added_setup_types:
            TypedSetup = get_model('feed', setup_name)
            setup = TypedSetup()
            setup.experiment = experiment
            setup.technique = Techniques.name2num(setup_name)
            # FIXME: should use request.user if available
            setup.created_by = experiment.created_by
            self._setups_to_save.append(setup)

        for setup_name in deleted_setup_types:
            setup = experiment.get_setup_by_type(setup_name, freshen=True)

            # If the setup has no sensors or channels, we can safely delete.
            if setup.sensor_set.count() == setup.channel_set.count() == 0:
                setup.delete()
            else:
                # We should show a message, but it is hard to do so from within
                # the form because we don't have access to the request object.
                pass

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

    def clean(self):
        cleaned_data = super(StudyChangeForm, self).clean()
        validate_start_end(cleaned_data)
        return cleaned_data


class SessionChangeForm(forms.ModelForm):
    class Meta:
        widgets = {
            'start': DateInput(attrs={'class':'datepicker'}),
            'end': DateInput(attrs={'class':'datepicker'}),
        }

    def clean(self):
        cleaned_data = super(SessionChangeForm, self).clean()
        validate_start_end(cleaned_data)
        return cleaned_data


class TrialChangeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(TrialChangeForm, self).clean()
        is_calibration = cleaned_data['is_calibration']
        behavior = cleaned_data['behaviorowl_primary']
        if behavior is None and not is_calibration:
            raise ValidationError('You must either check "Calibration" or choose a behavior')

        validate_start_end(cleaned_data)

        return cleaned_data

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
    name = CharField(label = "Name", widget=forms.TextInput(attrs={'size': 10}), help_text="Provide a short name for identifying the data contained in this Sensor.")
    notes = CharField(label ="Notes", widget=forms.Textarea(attrs={'cols': 8, 'rows': 2}), required=False)

    class Meta:
        fields = ['name', 'muscle', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'axisdepth', 'electrode_type', 'rate', 'unit', 'emg_filtering', 'emg_amplification',  'notes']

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


class ChannelLineupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['channel'].empty_label='dead channel'
        super(ChannelLineupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ChannelLineup


class StrainSensorForm(forms.ModelForm):
    notes = CharField(label="Notes",
        widget=forms.Textarea(),
        required=False,
        help_text="Notes including Gage Element Axial Orientation with specific information on gage placement (e.g., orientation of a gage element relative to a bone axis). Illustrations of gage placement can also be uploaded.")
