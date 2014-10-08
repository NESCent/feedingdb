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


def clone_session(session, experiment=None):
    """
    Modifies its argument to become the new session
    """
    copy_channels = True

    if experiment is not None:
        # we can't copy channels if we're changing experiment, because the channels
        # are part of the setup which is part of the experiment.
        #
        # TODO: when we're copying an experiment, we need to be able to clone
        # the channels while changing the experiment. Hrmph.
        copy_channels = False
        session.experiment = experiment

    trials = session.trial_set.all()
    if copy_channels:
        channels = session.channels.all()
        channellineups = session.channellineup_set.all()

    session.id = None
    session.pk = None
    session.save()
    for trial in trials:
        clone_trial(trial, session=session)

    if copy_channels:
        # If we can copy channels, that means we're using the same setup, so we
        # just need to copy the m2m relationships.
        #
        # Per Django docs, this would be a simple mapper of assigning the list
        # of channels to the new m2m field, but we have a `through` table, so
        # we have to make new relationships manually.
        for lineup in channellineups:
            clone_lineup(lineup, session=session)

def clone_trial(trial, session=None):
    _clone_basic(trial, session=session)

def clone_lineup(lineup, session=None):
    _clone_basic(lineup, session=session)

def _clone_basic(thing, **kwargs):
    thing.id = None
    thing.pk = None
    for key, value in kwargs:
        setattr(thing, key, value)
    thing.save()

