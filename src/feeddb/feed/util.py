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

    def get_dict(self):
        return self._data
