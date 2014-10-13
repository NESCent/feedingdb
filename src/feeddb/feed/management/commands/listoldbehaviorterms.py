from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import Trial, Behavior
from django.db.models import Q

class Command(BaseCommand):
    args = '<file>'
    help = 'help'

    def handle(self, *args, **options):
        print "pk, label, count_trials"
        for t in Behavior.objects.all():
            count = t.trial_set.count()
            print '"%s", "%s", "%s"' % (t.id, unicode(t), count)
