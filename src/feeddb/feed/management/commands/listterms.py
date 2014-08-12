from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import SonoSensor, EmgSensor, MuscleOwl, AnatomicalLocation
from django.db.models import Q

def sensors_with_al_missing_owl():
    sensors = set()
    for M in [SonoSensor, EmgSensor]:
        sensors |= set(M.objects.filter(
            location_controlled__isnull=False, 
            location_controlled__ontology_term__isnull=True
        ))
    return sensors


def used_terms():
    return AnatomicalLocation.objects.filter(
        Q(sonosensor__isnull=False) |
        Q(emgsensor__isnull=False)
    )

class Command(BaseCommand):
    args = '<file>'
    help = 'help'

    def handle(self, *args, **options):
        terms = set(used_terms().filter(ontology_term__isnull=True))
        print "pk, label, count_sensors"
        for t in terms:
            count = t.emgsensor_set.count() + t.sonosensor_set.count()
            print "%s, %s, %s" % (t.id, unicode(t), count)
