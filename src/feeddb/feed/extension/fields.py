"""
Customer form DateTimeField to set default time as 00:00:00 is not specified.
"""

from django.forms.fields import *
from django.contrib.admin.widgets import AdminSplitDateTime
import datetime
import time
from django.forms.util import ErrorList, ValidationError
from django.utils import formats


class FeedDateTimeField(Field):
    widget = AdminSplitDateTime
    def __init__(self, input_formats=None, *args, **kwargs):
        super(FeedDateTimeField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats or formats.get_format('DATETIME_FORMAT')
    
    def clean(self, value):
        """
        set default time to 00:00:00 if not specified
        """
        if value in (None,''):
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        if isinstance(value, list):
            # Input comes from a SplitDateTimeWidget, for example. So, it's two
            # components: date and time.
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid'])
            if value[0] in (None,'') and value[1] in (None,''):
                if self.required:
                    raise ValidationError(self.error_messages['invalid'])
                else:
                    return None    
            if value[1] in (None,''):
                value[1]="00:00:00"
            value = '%s %s' % tuple(value)
        
        for format in self.input_formats:
            try:
                return datetime.datetime(*time.strptime(value, format)[:6])
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])
