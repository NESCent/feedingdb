from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import MuscleOwl, AnatomicalLocation

class Command(BaseCommand):
    args = '<file>'
    help = 'help'

    def handle(self, filename, *args, **options):
        import csv
        
        qs = MuscleOwl.objects.filter(**MuscleOwl.default_qs_filter_args())

        with open(filename, 'rU') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                al_pk = row['pk']
                owl_uri = row['uri']
                owl_label = row['label MFMO FEED2 including new mammal muscles (yellow)']

                if al_pk:
                    al_pk = long(al_pk)
                    try:
                        try: 
                            match = qs.filter(label__iexact=owl_label).get()
                        except ObjectDoesNotExist:
                            match = qs.filter(label__iexact=(owl_label + " muscle")).get()
                    except ObjectDoesNotExist:
                        print "No match for %d" % al_pk
                        continue

                    al = AnatomicalLocation.objects.get(id=al_pk)
                    al.ontology_term = match
                    al.save()

