from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model

from feeddb.feed.cloning import *

from django.contrib.contenttypes.models import ContentType

# from feeddb.feed.management.commands import clone
class Command(BaseCommand):
    args = ''
    help = 'help'

    def handle(self, modelname, pk, **options):
        app = options.get('app', 'feed')
        obj = get_model(app, modelname).objects.get(pk=pk)
        if modelname == 'session':
            clone_session(obj)
        elif modelname == 'trial':
            clone_trial(obj)
        elif modelname == 'experiment':
            clone_experiment(obj)
        elif modelname == 'study':
            clone_study(obj)
