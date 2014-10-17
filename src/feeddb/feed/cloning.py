from feeddb.feed.models import SonoChannel, EventChannel
from django.conf import settings

def clone_supported_object(obj):
    modelname = type(obj).__name__.lower()
    if modelname == 'session':
        return clone_session(obj)
    elif modelname == 'trial':
        return clone_trial(obj)
    elif modelname == 'experiment':
        return clone_experiment(obj)
    elif modelname == 'study':
        return clone_study(obj)

def clone_study(study):
    experiments = study.experiment_set.all()
    subjects = study.subject_set.all()
    subjects_by_old_id = dict([(s.id, s) for s in subjects])

    _clone_basic(study)

    for subject in subjects:
        # modifies `subject` in place and thus modifies `subjects_by_old_id`
        subject.study = study
        _clone_basic(subject)

    for experiment in experiments:
        experiment.subject = subjects_by_old_id[experiment.subject.id]
        experiment.study = study
        clone_experiment(experiment)

def clone_experiment(experiment):
    sessions = list(experiment.session_set.all())
    setups = list(experiment.typed_setups())

    _clone_basic(experiment)

    for setup in setups:
        setup.experiment = experiment
        clone_setup(setup)

    for session in sessions:
        session.experiment = experiment
        clone_session(session)

def clone_setup(setup):
    # reverse foreign keys
    channels = list(setup.typed_channels())
    sensors = list(setup.typed_sensors())
    sensors_by_old_id  = dict([(s.id, s) for s in sensors])
    illustrations = list(setup.illustration_set.all())

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
    if settings.DEBUG:
        print "Old %s: %s (%d)" % (type(thing).__name__, thing, thing.pk)

    thing.id = None
    thing.pk = None
    if hasattr(thing, 'title'):
        thing.title = 'Clone of "%s"' % (thing.title)
    for key, value in kwargs.iteritems():
        setattr(thing, key, value)
    thing.save()

    if settings.DEBUG:
        print "New %s: %s (%d)" % (type(thing).__name__, thing, thing.pk)

