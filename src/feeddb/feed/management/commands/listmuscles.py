from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import SonoSensor, EmgSensor, MuscleOwl, AnatomicalLocation
from django.db.models import Q

class Command(BaseCommand):
    args = ''
    help = 'help'

    def handle(self, *args, **options):
        muscles = MuscleOwl.objects.filter(**MuscleOwl.default_qs_filter_args()).order_by('label')
        try:
            print "uri,label,obo_definition"
            for m in muscles:
                print "%s,%s,%s" % (m.uri, m.label, m.obo_definition)
        except IOError:
            """ Quit gracefully if there is a broken pipe or other output problem """
