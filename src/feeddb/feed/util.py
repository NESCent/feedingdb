from django.db.models.loading import get_model
from django.db.models import ForeignKey
from django.forms.models import ModelChoiceField
from UserDict import UserDict
# import the logging library
import logging
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
        logger.info(self._data.keys())

    def apply_defaults_to_form(self, form):
        logger.info(self._data.keys())
        for key, value in self._data.items():
            if form.fields.has_key(key):
                form.fields[key].initial = value

    def apply_defaults_to_instance(self, obj):
        for key, value in self._data.items():
            setattr(obj, key, value)

    def apply_restricted_querysets_to_form(self, form):
        """
        General version:
        For each field on the form, if it's referencing a model which has
        a model reference field referencing a model of the same type as one we have,
        then filter the list to include that.

        Current basic version: filter by study only
        """
        Study = get_model('feed', 'study')
        # iterate through fields on the form
        for field_name, field_value in form.fields.items():
            if isinstance(field_value, ModelChoiceField):
                M = field_value.queryset.model
                # iterate through 
                for Mfield in M._meta.fields:
                    if isinstance(Mfield, ForeignKey):
                        Parent = Mfield.related.parent_model
                        if Parent == Study:
                            kwargs = { Mfield.name: self._data['study'] }
                            form.fields[field_name].queryset = field_value.queryset.filter(**kwargs)

    def get_dict(self):
        return self._data

    @classmethod
    def current_study_view_url(cls, request):
        try:
            self = request.session['feed_upload_status']
            study_id = self._data['study']
            if study_id:
                return reverse_lazy('admin:feed_study_view', args=(study_id,))
        except (AttributeError, KeyError):
            pass

        return False
