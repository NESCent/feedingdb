from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model

from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    args = ''
    help = 'help'

    def handle(self, modelname, pk, **options):
        app = options.get('app', 'feed')
        obj = get_model(app, modelname).objects.get(pk)
        print_clone(obj)

def print_clone(obj):
    for related in obj._meta.get_all_related_objects()
        '''
        related.model -> Model class containing the relation
        related.field -> name of field on Model
        '''
        field_name = related.field.name
        filter_kwargs = { field_name: obj }
        related_objects = related.model.objects.filter(**filter_kwargs)
        # how do i avoid loading a trial, updating its study, then saving it
        # and having the save() method setting the study back to the study for
        # its session?
        #
        # conversely, i also need to avoid making two copies of the same trial. 
        #
        # this might mean some kind of network traversal, but i hope there is
        # something more straightforward. what about just keeping track of the
        # duplicated trials and running save() every time i make an update? it
        # might take three saves, but eventually it will be updated to point to
        # the right session, experiment, and study.

    for field in Model._meta.fields:
        if hasattr(field, 'related'):
            Parent = field.related.parent_model
            parent_type = ContentType.objects.get_for_model(s)
            parent_name = 
            if Parent == User:
                continue
            print_fields("%s.%s" % (prefix, field.name), Parent)
        else:
            print "%s.%s" % (prefix, field.name)
    
        
