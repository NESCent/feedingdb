from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import Trial
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = ''
    help = 'help'

    def handle(self, *args, **options):
        print_fields('object', Trial)

def print_fields(prefix, Model):
    for field in Model._meta.fields:
        if hasattr(field, 'related'):
            Parent = field.related.parent_model
            if Parent == User:
                continue
            print_fields("%s.%s" % (prefix, field.name), Parent)
        else:
            print "%s.%s" % (prefix, field.name)
                
