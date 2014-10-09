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
        obj = get_model(app, modelname).objects.get(pk)
        print_clone(obj)

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
    setups = experiment.setup_set.all()
    
def clone_setup(setup):
    # reverse foreign keys
    channels = setup.channel_set.all()
    sensors = setup.sensor_set.all()
    sensors_by_old_id  = dict([(s.id, s) for s in sensors])
    illustrations = setup.illustration_set.all()

    _clone_basic(setup)

    # trouble. each (typed) channel points to a typed sensor, and each sensor
    # also points to the setup. Not every sensor has to be used by a channel.

    for sensor in sensors:
        _clone_basic(sensor, setup=setup)
    for channel in channels:
        # TODO: I need to do different things for each channel and sensor type.
        # For example, SonoChannel objects have two sensors (crystal1 and
        # crystal2) but all the rest have a single sensor. And the sensor is
        # typed, so it probably doesn't work to assign an untyped sensor to the
        # attribute.
        if hasattr(channel, 'sonochannel'):
            new_crystal1 = sensors_by_old_id[channel.sonochannel.crystal1]
            new_crystal2 = sensors_by_old_id[channel.sonochannel.crystal2]
            _clone_basic(channel, setup=setup, crystal1=new_crystal1, crystal2=new_crystal2)
        else:
            # FIXME: use typed sensor and typed channel here. i.e. channel.emgchannel.sensor
            new_sensor = sensors_by_old_id[channel.sensor.id]
            _clone_basic(channel, setup=setup, sensor=new_sensor)

def clone_session(session):
    """
    Modifies its argument to become the new session
    """

    trials = session.trial_set.all()
    channellineups = session.channellineup_set.all()

    session.id = None
    session.pk = None
    session.save()
    for trial in trials:
        clone_trial(trial, session=session)

    # Per Django docs, this would be a simple mapper of assigning the list
    # of channels to the new m2m field, but we have a `through` table, so
    # we have to make new relationships manually.
    for lineup in channellineups:
        clone_lineup(lineup, session=session)

def clone_trial(trial):
    trial.title = 'Cloned Trial (was "%s")' % trial.title
    _clone_basic(trial)

def clone_lineup(lineup):
    _clone_basic(lineup)

def _clone_basic(thing, **kwargs):
    thing.id = None
    thing.pk = None
    for key, value in kwargs.iteritems():
        setattr(thing, key, value)
    thing.save()

