from django.db.models.loading import get_model
from django.db.models import ForeignKey
from django.forms.models import ModelChoiceField
from django.core.urlresolvers import reverse
from UserDict import UserDict
# import the logging library
import logging
from django.conf import settings

from feeddb.feed.models import Study, Experiment, Setup, TECHNIQUE_CHOICES_NAMED
#
# Get an instance of a logger
logger = logging.getLogger(__name__)

FIELDS = ('experiment', 'study', 'subject', 'session', 'trial')

class FeedUploadStatus():
    # TODO: Make sure we're only pickling IDs by overriding __getstate__ and __setstate__

    def __init__(self, session=None):
        self._session = session
        self._data = session.setdefault('feed_upload_status', {})

    def update_with_object(self, obj):
        name = type(obj).__name__.lower()
        if name in FIELDS:
            self._data[name] = obj
            self._session.modified = True

        for fname in FIELDS:
            if hasattr(obj, fname):
                self._data[fname] = getattr(obj, fname)
                self._session.modified = True

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
        """
        study = self._data.get('study', None)
        if study is None:
            return

        # iterate through fields on the form
        for field_name, field_value in form.fields.items():
            if isinstance(field_value, ModelChoiceField):
                M = field_value.queryset.model
                # iterate through
                for Mfield in M._meta.fields:
                    if isinstance(Mfield, ForeignKey):
                        Parent = Mfield.related.parent_model
                        if Parent == Study:
                            kwargs = { Mfield.name: study }
                            form.fields[field_name].queryset = field_value.queryset.filter(**kwargs)

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
