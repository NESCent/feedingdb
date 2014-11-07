from feeddb.feed.models import SonoChannel, EventChannel
from django.conf import settings

def clone_supported_object(obj, recurse=True):
    modelname = type(obj).__name__.lower()
    if modelname == 'session':
        return clone_session(obj, recurse=recurse)
    elif modelname == 'trial':
        return clone_trial(obj, recurse=recurse)
    elif modelname == 'experiment':
        return clone_experiment(obj, recurse=recurse)
    elif modelname == 'subject':
        return clone_subject(obj, recurse=recurse)
    elif modelname == 'study':
        return clone_study(obj, recurse=recurse)

def clone_study(study, recurse=True):
    subjects = study.subject_set.all()
    subjects_by_old_id = dict([(s.id, s) for s in subjects])
    if recurse:
        experiments = study.experiment_set.all()

    _clone_basic(study)

    for subject in subjects:
        # modifies `subject` in place and thus modifies `subjects_by_old_id`
        subject.study = study
        clone_subject(subject)

    if not recurse:
        return

    for experiment in experiments:
        experiment.subject = subjects_by_old_id[experiment.subject.id]
        experiment.study = study
        clone_experiment(experiment)

def clone_subject(subject, recurse=True):
    illustrations = list(subject.illustration_set.all())

    _clone_basic(subject)

    for illustration in illustrations:
        _clone_basic(illustration, subject=subject)

def clone_experiment(experiment, recurse=True):
    setups = list(experiment.typed_setups())
    illustrations = list(experiment.illustration_set.all())

    if recurse:
        sessions = list(experiment.session_set.all())

        # temp storage of channel map for use in session clone
        experiment.channels_by_old_id = dict()

    _clone_basic(experiment)


    for setup in setups:
        setup.experiment = experiment
        clone_setup(setup)

        # If we'll be cloning sessions later, we need to keep track of the
        # correspondence between old and new channels. See clone_session() and
        # clone_setup().
        if recurse:
            experiment.channels_by_old_id.update(setup.channels_by_old_id)

    for illustration in illustrations:
        _clone_basic(illustration, experiment=experiment)

    if not recurse:
        return

    for session in sessions:
        session.experiment = experiment
        clone_session(session)


def clone_setup(setup):
    # reverse foreign keys
    channels = list(setup.typed_channels())
    sensors = list(setup.typed_sensors())
    sensors_by_old_id = dict([(s.id, s) for s in sensors])
    channels_by_old_id = dict([(c.id, c) for c in channels])
    illustrations = list(setup.illustration_set.all())

    _clone_basic(setup)

    for sensor in sensors:
        # This modifies `sensor` in place, so `sensors_by_old_id` will contain
        # the new sensors when this loop finishes.
        _clone_basic(sensor, rename=False, setup=setup)

    for channel in channels:
        # Each channel type has a different type of sensor, but, with the
        # exception of SonoChannels and EventChannels, they are all stored on
        # the same attribute
        if type(channel) == SonoChannel:
            new_crystal1 = sensors_by_old_id[channel.crystal1.id]
            new_crystal2 = sensors_by_old_id[channel.crystal2.id]
            _clone_basic(channel, rename=False, setup=setup, crystal1=new_crystal1, crystal2=new_crystal2)
        elif type(channel) == EventChannel:
            # Event channels don't have sensors
            _clone_basic(channel, rename=False, setup=setup)
        elif hasattr(channel, 'sensor'):
            # This is for most channel types
            old_sensor = channel.sensor
            new_sensor = sensors_by_old_id[old_sensor.id]
            _clone_basic(channel, rename=False, setup=setup, sensor=new_sensor)
        else:
            raise ValueError("Channel %s (pk=%d) is of unknown type %s" % (channel, channel.pk, type(channel)))

    for illustration in illustrations:
        _clone_basic(illustration, setup=setup)

    # save these dicts to the setup so clone_experiment() can use it later.
    setup.sensors_by_old_id = sensors_by_old_id
    setup.channels_by_old_id = channels_by_old_id

def clone_session(session, recurse=True):
    """
    Modifies its argument to become the new session
    """

    channellineups = session.channellineup_set.all()
    if recurse:
        trials = session.trial_set.all()

    _clone_basic(session)

    if not recurse:
        return

    for trial in trials:
        trial.session = session
        clone_trial(trial)

    # Per Django docs, this would be a simple mapper of assigning the list
    # of channels to the new m2m field, but we have a `through` table, so
    # we have to make new relationships manually.
    for lineup in channellineups:
        if settings.DEBUG:
            print "Old lineup: Pos %d, Chan %s (pk=%d)" % (lineup.position, lineup.channel, lineup.channel.pk)
        lineup.session = session

        # If we're in an experiment clone (or study clone), there will be new
        # channels and we need to update the lineup to refer to the new
        # channels. See clone_experiment() and clone_setup().
        if hasattr(session.experiment, 'channels_by_old_id'):
            lineup.channel = session.experiment.channels_by_old_id[lineup.channel.id]
        clone_lineup(lineup)

def clone_trial(trial, recurse=True):
    trial.data_file = None
    trial.waveform_picture = None
    _clone_basic(trial)

def clone_lineup(lineup):
    _clone_basic(lineup)
    if settings.DEBUG:
        print "New lineup: Pos %d, Chan %s (pk=%d)" % (lineup.position, lineup.channel, lineup.channel.pk)

def _clone_basic(thing, rename=True, **kwargs):
    if settings.DEBUG:
        print "Old %s: %s (%d)" % (type(thing).__name__, thing, thing.pk)

    thing.id = None
    thing.pk = None
    if rename:
        if hasattr(thing, 'title'):
            thing.title = 'Clone of "%s"' % (thing.title)
        if hasattr(thing, 'name'):
            thing.name = 'Clone of "%s"' % (thing.name)

    for key, value in kwargs.iteritems():
        setattr(thing, key, value)
    thing.save()

    if settings.DEBUG:
        print "New %s: %s (%d)" % (type(thing).__name__, thing, thing.pk)

