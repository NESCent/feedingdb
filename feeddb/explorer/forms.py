from django import forms
from feeddb.feed.models import *

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
 