from django import forms
from feeddb.feed.models import *
from feeddb.explorer.models import *

SPECIES_CHOICES = [('','')]
MUSCLE_CHOICES=[('','')]
SENSOR_CHOICES=[('','')]
BEHAVIOR_CHOICES=[('','')]



for s in Taxon.objects.all():
    SPECIES_CHOICES.append((s.id, '%s %s' % (s.genus, s.species)))

for s in Muscle.objects.all():
    MUSCLE_CHOICES.append((s.id, s.label))

for s in Technique.objects.all():
    SENSOR_CHOICES.append((s.id, s.label))

for s in Behavior.objects.all():
    BEHAVIOR_CHOICES.append((s.id, s.label))


class SearchTrailForm (forms.Form):
    species = forms.ChoiceField(choices=SPECIES_CHOICES,required=False)
    muscle = forms.ChoiceField(choices=MUSCLE_CHOICES,required=False)
    #bone =forms.ChoiceField(required=False)
    sensor = forms.MultipleChoiceField(choices=SENSOR_CHOICES,required=False)
    primary_behavior=forms.ChoiceField(choices=BEHAVIOR_CHOICES,required=False)
    food_type=forms.CharField(max_length=100,required=False)
 
class BucketModelForm(forms.ModelForm):
    class Meta:
        model = Bucket
        exclude = ('trials',)

class StudyModelForm(forms.ModelForm):
    class Meta:
        model=Study
        name = 'Study'

class SubjectModelForm(forms.ModelForm):
    class Meta:
        model=Subject
        exclude = ('study',)
        name = 'Subject'

class ExperimentModelForm(forms.ModelForm):
    class Meta:
        model=Experiment
        exclude = ('study','subject',)
        name = 'Experiment'

class SessionModelForm(forms.ModelForm):
    class Meta:
        model=Session
        exclude = ('experiment','channels')
        name = 'Session'

class TrialModelForm(forms.ModelForm):
    class Meta:
        model=Trial
        exclude = ('session',)
        name = 'Trial'
