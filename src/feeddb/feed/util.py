from django.db.models.loading import get_model
from django.db.models import ForeignKey
from django.forms.models import ModelChoiceField
from django.core.urlresolvers import reverse
from UserDict import UserDict
# import the logging library
import logging
from django.conf import settings

from feeddb.feed.models import Study, Subject, Experiment, Setup, Session, Trial
#
# Get an instance of a logger
logger = logging.getLogger(__name__)

# These are the lowercase names of the model instances which we track, in order
# of containing to contained. We can omit 'trial' because trials don't contain
# anything.
FIELDS = ('study', 'subject', 'experiment', 'session')

class FeedUploadStatus():
    # TODO: Make sure we're only pickling IDs by overriding __getstate__ and __setstate__

    def __init__(self, session=None):
        self._session = session
        self._data = session.setdefault('feed_upload_status', {})

    def update_with_object(self, obj):
        """
        Update our "current objects" cache with the given object and all of the values
        in any fields named in FIELDS.

        We only expect to be called with a Study, Subject, Experiment, Session,
        or Trial. Anything else might have weird results.
        """
        if type(obj) not in (Study, Subject, Experiment, Session, Trial):
            if isinstance(obj, Setup):
                pass
            else:
                raise TypeError('Cannot update FeedUploadStatus with object of type %s' % type(obj))

        name = type(obj).__name__.lower()
        if name in FIELDS:
            self._data[name] = obj
            self._session.modified = True

        # When visiting a trial page, we should fill in all the parents.
        # However, when visiting a subject page, we should clear the saved
        # experiment, session, and trial.
        #
        # Why? For one, it might be part of a different study. For another, it
        # would produce weird results if the next page is an "add" page for a
        # trial or session.
        clear_the_rest = False
        for fname in FIELDS:
            if clear_the_rest:
                try:
                    del self._data[fname]
                    self._session.modified = True
                except KeyError:
                    pass
            elif hasattr(obj, fname):
                val = getattr(obj, fname)
                # support function attributes
                if callable(val):
                    val = val()
                self._data[fname] = val
                self._session.modified = True
            else:
                clear_the_rest = True

        logger.info(self._data.keys())

    def apply_defaults_to_form(self, form):
        logger.info(self._data.keys())
        for key, value in self._data.items():
            if form.fields.has_key(key):
                form.fields[key].initial = value

    def apply_defaults_to_instance(self, obj):
        for key, value in self._data.items():
            setattr(obj, key, value)

    def object_is_in_study(self, obj):
        try:
            study = self._data['study']
            if isinstance(obj, Study):
                return study == obj
            else:
                return study == obj.study
        except (KeyError, AttributeError):
            # Either we don't have a stored study or the object isn't a Study
            # and doesn't have a 'study' attribute
            pass

        return False


    def apply_restricted_querysets_to_form(self, form):
        """
        General version:
        For each field on the form, if it's referencing a model which has
        a model reference field referencing a model of the same type as one we have,
        then filter the list to include that.

        Current basic version: filter by study only
        TODO: add filtering by experiment (for channel selector and ???)

        Perhaps by this method: on each form field, look first for a trial,
        then a session, then an experiment.

        or perhaps by hard-coding the logic for each thing.
        """
        study = self._data.get('study', None)
        if study is None:
            return

        Model = type(form.instance)

        # iterate through fields on the form
        for field_name, field_value in form.fields.items():
            logger.info('on field %s', field_name)
            if isinstance(field_value, ModelChoiceField):
                M = field_value.queryset.model
                qs_args = dict(self.args_applicable_to_model(M))
                if len(qs_args):
                    form.fields[field_name].queryset = field_value.queryset.filter(**qs_args)

    def args_applicable_to_model(self, Model):
        """
        Given a model, yield name-value pairs which would apply to a query on that model,
        based on the data we have.

        For each field on the model, check if we have a value by that name. If
        we do, yield the (name, value) pair.

        In addition, we have special cases for fields which are FKs to things
        which have FKs to the things we know about.

        """
        for field in Model._meta.fields:
            try:
                if field.name == 'setup' and isinstance(field, ForeignKey):
                    yield ('setup__experiment', self._data['experiment'])
                else:
                    yield (field.name, self._data[field.name])
            except KeyError:
                # If we can't look it up in self._data, don't worry about it.
                pass


    def get_dict(self):
        return self._data

    @classmethod
    def current_study_view_url(cls, request, form_data, obj):
        try:
            self = request.feed_upload_status
            study = self._data['study']
            if study:
                return reverse('admin:feed_study_view', args=(study.id,))
        except (AttributeError, KeyError):
            pass

        return False

    @classmethod
    def next_setup_or_session_url(cls, request, form_data, obj):
        try:
            self = request.feed_upload_status
            study = self._data['study']
            logger.info('study %s' % study.id)
            if type(obj) == Experiment and obj.study == study:
                experiment = obj

                if settings.DEBUG:
                    logger.info('experiment %s' % experiment.id)
                    logger.info('s with t %s' % unicode(experiment.get_setups_with_type(freshen=True)))
                    logger.info('s %s' % unicode([s.id for s in experiment.get_setups(freshen=True)]))

                for setup_name, setup in experiment.get_setups_with_type(freshen=True):
                    return reverse('admin:feed_%s_change' % setup_name, args=(setup.id,))
                else:
                    return reverse('admin:feed_session_add')
            elif isinstance(obj, Setup):
                experiment = obj.experiment

                if settings.DEBUG:
                    logger.info('experiment %s' % experiment.id)
                    logger.info('s with t %s' % unicode(experiment.get_setups_with_type(freshen=True)))
                    logger.info('s %s' % unicode([s.id for s in experiment.get_setups(freshen=True)]))
                    logger.info("isinstaance setup %d" % obj.id)

                this_is_next = False
                for setup_name, setup in experiment.get_setups_with_type(freshen=True):
                    if this_is_next:
                        return reverse('admin:feed_%s_change' % setup_name, args=(setup.id,))
                    if setup.id == obj.id:
                        this_is_next = True
                else:
                    return reverse('admin:feed_session_add')
            logger.info("didn't send any url")

        except (AttributeError, KeyError):
            pass

        return False
