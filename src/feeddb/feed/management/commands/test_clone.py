from django.test import TestCase
from feeddb.feed.management.commands import clone
from feeddb.feed.models import Trial, Session, Experiment, Study

class CloningTestCase(TestCase):
    fixtures = [ 'test-feed-all-models' ]

    def setUp(self):
        pass

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

    def test_clone_trial(self):
        #####
        # Make a simple clone within the same session
        old_trial = Trial.objects.get(id=201)
        new_trial = Trial.objects.get(id=201)
        clone.clone_trial(new_trial)
        self.assertTrialsDiffer(old_trial, new_trial)

        #####
        # Make a clone and assign it to another session
        experiment = old_trial.session.experiment
        other_session = experiment.session_set.objects.exclude(id=old_trial.session.id).first()

        new_trial = Trial.objects.get(id=201)
        clone.clone_trial(new_trial, session=other_session)

        self.assertTrialsDiffer(old_trial, new_trial)

        self.assertEqual(new_trial.session.id, other_session.id,
            "New trial with other session is part of other session")

        # reload trial from database ... should check this is necessary.
        new_trial = Trial.objects.get(id=new_trial.id)
        self.assertTrialsDiffer(old_trial, new_trial)

        self.assertEqual(new_trial.session.id, other_session.id,
            "New trial with other session is part of other session")

    def test_clone_session(self):
        # Make a simple clone within the same experiment
        old_session = Session.objects.get(id=190)
        new_session = Session.objects.get(id=190)
        clone.clone_session(new_session)
        self.assertSessionsDiffer(old_session, new_session)
