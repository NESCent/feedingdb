from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import SonoSensor, EmgSensor, MuscleOwl, AnatomicalLocation
from django.db.models import Q
from django.db.models.loading import get_model

class Command(BaseCommand):
    args = 'model'
    help = 'help'

    def handle(self, *args, **options):
        try:
            name = args[0]
        except IndexError:
            name = 'muscleowl'

        Model = get_model('feed', name)

        terms = Model.objects.filter(**Model.default_qs_filter_args()).order_by('label')
        try:
            print "uri,label,obo_definition"
            for t in terms:
                print "%s,%s,%s" % (t.uri, t.label, t.obo_definition)
        except IOError:
            """ Quit gracefully if there is a broken pipe or other output problem """
