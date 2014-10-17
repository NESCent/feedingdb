from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model

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

def print_clone(obj):
    for related in obj._meta.get_all_related_objects():
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

def _dict_by_attr(objects, attr):
    return dict([(getattr(o, attr), o) for o in objects])

def clone_experiment(experiment):
    sessions = experiment.session_set.all()
    setups = experiment.typed_setups()

    _clone_basic(experiment)

    for setup in setups:
        setup.experiment = experiment
        clone_setup(setup)

    for session in sessions:
        session.experiment = experiment
        clone_session(session)

def clone_setup(setup):
    # reverse foreign keys
    channels = setup.typed_channels()
    sensors = setup.typed_sensors()
    sensors_by_old_id  = dict([(s.id, s) for s in sensors])
    illustrations = setup.illustration_set.all()

    _clone_basic(setup)

    for sensor in sensors:
        # This modifies `sensor` in place, so `sensors_by_old_id` will contain
        # the new sensors when this loop finishes.
        _clone_basic(sensor, setup=setup)
    for channel in channels:
        # Each channel type has a different type of sensor, but, with the
        # exception of SonoChannels and EventChannels, they are all stored on
        # the same attribute
        if type(channel) == SonoChannel:
            new_crystal1 = sensors_by_old_id[channel.crystal1.id]
            new_crystal2 = sensors_by_old_id[channel.crystal2.id]
            _clone_basic(channel, setup=setup, crystal1=new_crystal1, crystal2=new_crystal2)
        elif type(channel) == EventChannel:
            _clone_basic(channel, setup=setup)
        elif hasattr(channel, 'sensor'):
            # This is for most channel types
            old_sensor = channel.sensor
            new_sensor = sensors_by_old_id[old_sensor.id]
            _clone_basic(channel, setup=setup, sensor=new_sensor)
        else:
            raise ValueError("Channel %s (pk=%d) is of unknown type %s" % (channel, channel.pk, type(channel)))

def clone_session(session):
    """
    Modifies its argument to become the new session
    """

    trials = session.trial_set.all()
    channellineups = session.channellineup_set.all()

    _clone_basic(session)

    for trial in trials:
        trial.session = session
        clone_trial(trial)

    # Per Django docs, this would be a simple mapper of assigning the list
    # of channels to the new m2m field, but we have a `through` table, so
    # we have to make new relationships manually.
    for lineup in channellineups:
        lineup.session = session
        clone_lineup(lineup)

def clone_trial(trial):
    _clone_basic(trial)

def clone_lineup(lineup):
    _clone_basic(lineup)

def _clone_basic(thing, **kwargs):
    print "Old %s: %s (%d)" % (type(thing).__name__, thing, thing.pk)
    thing.id = None
    thing.pk = None
    if hasattr(thing, 'title'):
        thing.title = 'Clone of "%s"' % (thing.title)
    for key, value in kwargs.iteritems():
        setattr(thing, key, value)
    thing.save()
    print "New %s: %s (%d)" % (type(thing).__name__, thing, thing.pk)

