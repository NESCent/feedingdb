from haystack.forms import FacetedSearchForm
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.query import RelatedSearchQuerySet
from inspector_panel import debug
from django import forms
from django.forms.fields import ChoiceField, BooleanField
from django.forms.widgets import RadioSelect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict, fields_for_model
from collections import OrderedDict

from django.contrib.auth.models import User

from feeddb.feed.models import Trial, Session, Experiment, Subject, Study, FeedUserProfile

from faceted_search.searcher import Searcher

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

my_facet_config = {
    'fields': {
        'analoc': { 'label': 'Anatomical Location' },
        'behaviorowl_primary_ancestors': { 'label': 'Primary Behavior' },
        'taxon': { 'label': 'Species' },
        'food_type': { 'label': 'Food Type' },
        'techniques': { 'label': 'Sensor Type' },
    }
}

class UserOwnProfileForm(forms.ModelForm):
    _user_fields = ('email', 'first_name', 'last_name')
    _field_order = ('first_name', 'last_name', 'email', 'institutional_affiliation')

    def __init__(self, initial=None, instance=None, *args, **kwargs):
        _user_initial = model_to_dict(instance.user, self._user_fields) if instance is not None else {}
        initial.update(_user_initial)
        super(UserOwnProfileForm, self).__init__(initial=initial, instance=instance, *args, **kwargs)
        self.fields.update(fields_for_model(User, self._user_fields))

        # reorder fields according to order above
        self.fields = OrderedDict((k, self.fields[k]) for k in self._field_order)

    class Meta:
        model = FeedUserProfile

    def save(self, *args, **kwargs):
        u = self.instance.user
        for field in self._user_fields:
            setattr(u, field, self.cleaned_data[field])
        u.save()
        profile = super(UserOwnProfileForm, self).save(*args, **kwargs)
        return profile


class ModelCloneForm(forms.Form):
    source = forms.ModelChoiceField(queryset=None)
    recurse = forms.BooleanField(required=False)

    def __init__(self, container=None, *args, **kwargs):
        self.clone_subject = kwargs.pop('clone_subject', False)

        super(ModelCloneForm, self).__init__(*args, **kwargs)

        ContainerModel = type(container)

        if ContainerModel == Session:
            qs = Trial.objects.filter(session=container)
        elif ContainerModel == Experiment:
            qs = Session.objects.filter(experiment=container)
        elif ContainerModel == Study:
            if self.clone_subject:
                qs = Subject.objects.filter(study=container)
            else:
                qs = Experiment.objects.filter(study=container)
        elif container == None:
            qs = Study.objects.all()
        else:
            raise ValueError("ModelCloneForm does not support container model type %s" % ContainerModel)

        self.fields['source'].queryset = qs
        self.feed_source_count = len(qs)
        self.container = container

    def action_url(self):
        "Get url for action attribute of form tag. See ../urls.py"
        if self.container == None:
            return reverse('clone_study')
        elif self.clone_subject:
            kwargs = {
                'container_pk': self.container.pk,
            }
            return reverse('clone_subject_from_study', kwargs=kwargs)
        else:
            kwargs = {
                'container_type': type(self.container).__name__.lower(),
                'container_pk': self.container.pk,
            }
            return reverse('clone_from_container', kwargs=kwargs)

    @classmethod
    def factory(cls, modeladmin, request):
        # fake context so I can re-use get_current_containers()
        context = {
            'opts': modeladmin.model._meta,
            'request': request
        }
        from feeddb.feed.templatetags.upload_status import get_current_containers
        containers = get_current_containers(context)

        try:
            # move down the tree until they don't exist anymore
            container = None
            container = containers['study']
            container = containers['experiment']
            container = containers['session']
        except KeyError:
            pass

        # Special case for subject, because its container is the same as when
        # cloning an experiment.
        if context['opts'].model_name == 'subject':
            return cls(container=container, clone_subject=True, prefix='clone')
        else:
            return cls(container=container, prefix='clone')

class FeedSearchForm(FacetedSearchForm):
    per_page = ChoiceField(
        choices=[(n, n) for n in (10, 30, 50, 100, 200)],
        initial=10,
        widget=RadioSelect(),
    )

    def __init__(self, GET, *args, **kwargs):
        # Save all GET parameters in case they match facets and not form fields
        self.filters = GET

        super(FeedSearchForm, self).__init__(GET, *args, **kwargs)
        self.searcher = Searcher(model=Trial, facets=my_facet_config, queryset=RelatedSearchQuerySet())

    def no_query_found(self):
        """
        Override no_query_found behavior to return all results when no keyword
        search is provided
        """
        return self.searchqueryset.all()

    def search(self):
        # Get keywords from form, defaulting to empty string
        try:
            q = self.cleaned_data['q']
        except (AttributeError, KeyError): # if self.cleaned_data doesn't exist
            q = ''

        sqs = self.searcher.search(filters=self.filters, keywords=q)

        sqs = sqs.order_by('taxon')

        sqs = sqs.load_all()

        return sqs
