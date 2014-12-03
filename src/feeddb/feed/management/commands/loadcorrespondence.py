from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import MuscleOwl, BehaviorOwl, Behavior, AnatomicalLocation, EmgSensor, SonoSensor, Trial

class Command(BaseCommand):
    args = '<m|b> <file>'
    help = 'help'

    def handle(self, model_char, filename, *args, **options):
        import csv
        if model_char == 'm':
            Owl = MuscleOwl
            CvTerm = AnatomicalLocation
        elif model_char == 'b':
            Owl = BehaviorOwl
            CvTerm = Behavior
        else:
            print "Must specify Muscles (m) or Behavior (b) as first argument."
            return

        qs = Owl.default_qs()

        with open(filename, 'rU') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                try:
                    cv_pk = long(row['pk'])
                    owl_uri = row['uri']
                except ValueError:
                    # usually means that row['pk'] is not a valid long; skip
                    # this row.
                    continue

                try:
                    cvterm = CvTerm.objects.get(id=cv_pk)
                except CvTerm.DoesNotExist:
                    print "Cannot find CvTerm with pk=%d; would migrate to uri: '%s'" % (cv_pk, owl_uri)
                    continue

                try:
                    match = qs.get(uri__iexact=owl_uri)
                except ObjectDoesNotExist:
                    print "No match for uri '%s'; would have migrated from pk=%d" % (owl_uri, cv_pk)
                    match = None

                cvterm.ontology_term = match
                cvterm.save()


        if Owl == MuscleOwl:
            # Now we can update the actual sensors. We assume that the
            # location_controlled value is more "correct" than the muscle field
            # on all sensors with a non-null location_controlled value.
            #
            # In other words, sensors with a null location_controlled value are
            # not clobbered because they are expected to be FEED2 data (either
            # test or real)
            for Sensor in (EmgSensor, SonoSensor):
                for s in Sensor.objects.filter(location_controlled__isnull=False):
                    s.muscle = s.location_controlled.ontology_term
                    s.save()

        if Owl == BehaviorOwl:
            # We ignore trials with null behaviors in the belief that they are
            # FEED2 data.
            for trial in Trial.objects.filter(behavior_primary__isnull=False):
                trial.behaviorowl_primary = trial.behavior_primary.ontology_term
                trial.save()

