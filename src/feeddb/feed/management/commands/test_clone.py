from django.test import TestCase
from feeddb.feed.management.commands import clone
from feeddb.feed.models import Trial, Session, Experiment, Study

class CloningTestCase(TestCase):
    fixtures = [ 'test-feed-all-models', 'test-users' ]

    def setUp(self):
        pass

    def assertListsDistinct(self, left, right)
        left_ids = [t.id for t in left]
        right_ids = [t.id for t in right]
        for id in left_ids:
            self.assertNotIn(id, right_ids)

    def assertTrialsDiffer(self, old_trial, new_trial):
        self.assertNotEqual(old_trial.id, new_trial.id,
            "New trial has new ID")
        self.assertNotEqual(old_trial.title, new_trial.title,
            "New trial has new title")

    def assertSessionsDiffer(self, old_session, new_session):
        self.assertNotEqual(old_session.id, new_session.id,
            "New session has new ID")
        self.assertNotEqual(old_session.title, new_session.title,
            "New session has new title")

        self.assertListsDistinct(old_session.trial_set.all(), new_session.trial_set.all())
        self.assertListsDistinct(old_session.channellineup_set.all(), new_session.channellineup_set.all())

    def assertExperimentsDiffer(self, old_experiment, new_experiment):
        self.assertNotEqual(old_experiment.id, new_experiment.id,
            "New experiment has new ID")
        self.assertNotEqual(old_experiment.title, new_experiment.title,
            "New experiment has new title")

        self.assertListsDistinct(old_experiment.session_set.all(), new_experiment.session_set.all())
        self.assertListsDistinct(old_experiment.typed_setups(), new_experiment.typed_setups())

        def exp_sensors(exp):
            for setup in exp.typed_setups():
                for sensor in setup.typed_sensors():
                    yield sensor
        self.assertListsDistinct(exp_sensors(old_experiment), exp_sensors(new_experiment))

        def exp_channels(exp):
            for setup in exp.typed_setups():
                for channel in setup.typed_channels():
                    yield channel
        self.assertListsDistinct(exp_channels(old_experiment), exp_channels(new_experiment))

    def assertStudiesDiffer(self, old_study, new_study):
        for old_experiment in old_study.experiment_set.all()
            for new_experiment in new_study.experimnen_set.all():
                self.assertExperimentsDiffer(old_experiment, new_experiment)

        self.assertListsDistinct(old_study.subject_set.all(), new_study.subject_set.all())

    def test_clone_trial(self):
        #####
        # Make a simple clone within the same session
        old_trial = Trial.objects.get(id=201)
        new_trial = Trial.objects.get(id=201)
        clone.clone_trial(new_trial)
        self.assertTrialsDiffer(old_trial, new_trial)

    def test_clone_session(self):
        # Make a simple clone within the same experiment
        old_session = Session.objects.get(id=190)
        new_session = Session.objects.get(id=190)
        clone.clone_session(new_session)
        self.assertSessionsDiffer(old_session, new_session)

    def test_clone_experiment(self):
        old_experiment = Experiment.objects.get(id=196)
        new_experiment = Experiment.objects.get(id=196)
        clone.clone_experiment(new_experiment)
        self.assertExperimentsDiffer(old_experiment, new_experiment)

    def test_clone_study(self):
        old_study = Study.objects.get(id=196)
        new_study = Study.objects.get(id=196)
        clone.clone_study(new_study)
        self.assertStudiesDiffer(old_study, new_study)
