from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import MuscleOwl, AnatomicalLocation, EmgSensor, SonoSensor

class Command(BaseCommand):
    args = '<file>'
    help = 'help'

    def handle(self, filename, *args, **options):
        import csv

        qs = MuscleOwl.objects.filter(**MuscleOwl.default_qs_filter_args())

        with open(filename, 'rU') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                try:
                    al_pk = long(row['pk'])
                    owl_uri = row['uri']
                except ValueError:
                    # usually means that row['pk'] is not a valid long; skip
                    # this row.
                    continue

                al = AnatomicalLocation.objects.get(id=al_pk)
                if al:
                    try:
                        match = qs.filter(uri__iexact=owl_uri).get()
                    except ObjectDoesNotExist:
                        print "No match for %d: %s" % (al_pk, owl_uri)
                        match = None

                    al.ontology_term = match
                    al.save()

        # Now we can update the actual sensors
        for Sensor in (EmgSensor, SonoSensor):
            for s in Sensor.objects.filter(location_controlled__ontology_term__isnull=False):
                s.muscle = s.location_controlled.ontology_term
                s.save()

