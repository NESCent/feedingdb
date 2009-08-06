import copy

from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse, NoReverseMatch
from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.forms.util import flatatt
from django.utils.text import truncate_words
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.conf import settings

class FeedRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    def __init__(self, widget, rel, admin_site):
        super(FeedRelatedFieldWidgetWrapper, self).__init__(widget, rel, admin_site)

    def render(self, name, value, *args, **kwargs):
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        try:
            related_url = reverse('admin:%s_%s_add' % info, current_app=self.admin_site.name)
        except NoReverseMatch:
            info = (self.admin_site.root_path, rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = '%s%s/%s/add/' % info
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        return mark_safe(u''.join(output))

