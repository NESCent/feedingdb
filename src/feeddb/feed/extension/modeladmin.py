from django.contrib import admin
from feeddb.feed.extension.widgets import FeedRelatedFieldWidgetWrapper
from django import forms, template
from django.core.urlresolvers import reverse_lazy
from django.forms.formsets import all_valid
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.forms.formsets import formset_factory
from django.forms.models import BaseInlineFormSet
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import widgets
from django.contrib.admin import helpers
from django.contrib.admin.util import unquote, flatten_fieldsets, get_deleted_objects, model_ngettext, model_format_dict
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.db.models.fields import BLANK_CHOICE_DASH
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.datastructures import SortedDict
from functools import update_wrapper
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.functional import curry
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext, ugettext_lazy
from django.utils.encoding import force_unicode
from feeddb.feed.util import FeedUploadStatus
from feeddb.feed.models import  *
from feeddb.feed.forms import *
from feeddb.explorer.models import  *
from feeddb.feed.extension.forms import *
from feeddb.feed.extension.formsets import PositionBaseInlineFormSet
from django.forms.util import ValidationError
from feeddb.feed.extension.changelist import *
from feeddb.feed.extension.util import *
from django.template import RequestContext
from django.contrib.admin.views.main import IncorrectLookupParameters
from django.contrib import messages

#for 1.2.4
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from feeddb.feed.util import FeedAdminUtils

csrf_protect_m = method_decorator(csrf_protect)
#end for 1.2.4

class FeedTabularInline(admin.TabularInline):
    template = 'admin/edit_inline/tabular.html'
    #change_form_template = 'admin/tabbed_change_form.html'
    tabbed = False
    tab_name = None

    def has_change_permission(self, request, obj=None):
        change_all = super(FeedTabularInline, self).has_change_permission(request, obj)
        return change_all or FeedAdminUtils.has_instance_change_permission(request, obj)

    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs.pop("request", None)

        if db_field.choices:
            return self.formfield_for_choice_field(db_field, request, **kwargs)

        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            if db_field.__class__ in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[db_field.__class__], **kwargs)

            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)
            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(db_field, request, **kwargs)

            if formfield and db_field.name not in self.raw_id_fields:
                formfield.widget = FeedRelatedFieldWidgetWrapper(formfield.widget, db_field.rel, self.admin_site)

            return formfield

        for klass in db_field.__class__.mro():
            if klass in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[klass], **kwargs)
                return db_field.formfield(**kwargs)

        return db_field.formfield(**kwargs)

class SetupTabularInline(FeedTabularInline):
    template = 'admin/edit_inline/setup_tabular.html'

class FeedModelAdmin(admin.ModelAdmin):
    view_inlines = []
    list_per_page = 30
    list_max_show_all = 100
    # Custom templates (designed to be over-ridden in subclasses)
    view_form_template = None
    #change_form_template = "admin/tabbed_change_form.html"
    # Actions
    actions = None

    # tabbed view?
    tabbed = False
    tab_name = None

    # Redirect destinations for "next step" functionality.
    #
    # These destinations have to be specified here rather than in the template
    # for both technical reasons and for security reasons. Destinations are
    # chosen by adding a submit button to the form with a `name` attribute
    # equal to "_redirect_" followed by the key in the success_destinations
    # dictionary. For example:
    #
    # In your template, add the special button:
    #   <input type="submit" name="_redirect_MY_DESTINATION" value="Save and go to my destination">
    # Then add the redirection URL here:
    #   success_destinations = { 'MY_DESTINATION': 'some/url/to/which/to/redirect' }
    #
    # These redirects are currently used only on "add" and "change" responses
    # which are not delivered to popup windows.  See
    # get_redirect_destination(), response_add(), and response_change()
    success_destinations = {
        'add_experiment': reverse_lazy('admin:feed_experiment_add'),
        'add_trial': reverse_lazy('admin:feed_trial_add'),
        'add_session': reverse_lazy('admin:feed_session_add'),
        'add_subject': reverse_lazy('admin:feed_subject_add'),
        'study_view': FeedUploadStatus.current_study_view_url,
        'setup_or_session': FeedUploadStatus.next_setup_or_session_url,
    }

    def __init__(self, model, admin_site):
        super(FeedModelAdmin, self).__init__(model,admin_site)
        self.view_inline_instances = []
        for view_inline_class in self.view_inlines:
            view_inline_instance = view_inline_class(self.model, self.admin_site)
            self.view_inline_instances.append(view_inline_instance)

    def get_redirect_destination(self, request, form_data, obj, default=''):
        import logging

        # Get an instance of a logger
        logger = logging.getLogger(__name__)
        ret = False
        if self.success_destinations:
            for name in self.success_destinations:
                if '_redirect_' + name in form_data:
                    logger.info("trying %s" % name)
                    if callable(self.success_destinations[name]):
                        logger.info("calling %s" % name)
                        ret = self.success_destinations[name](request, form_data, obj)
                    else:
                        ret = self.success_destinations[name]
        return ret or default

    def save_model(self, request, obj, form, change):
        if not change:
            request.feed_upload_status.apply_defaults_to_instance(form.instance);
        form.save();
        request.feed_upload_status.update_with_object(form.instance, fail_silently=True)

    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^add/$',
                wrap(self.add_view),
                name='%s_%s_add' % info),
            url(r'^(.+)/history/$',
                wrap(self.history_view),
                name='%s_%s_history' % info),
            url(r'^(.+)/delete/$',
                wrap(self.delete_view),
                name='%s_%s_delete' % info),
            url(r'^(.+)/edit/$',
                wrap(self.change_view),
                name='%s_%s_change' % info),
            url(r'^(.+)/clone/$',
                wrap(self.clone_view),
                name='%s_%s_clone' % info),
            url(r'^(.+)/$',
                wrap(self.view_view),
                name='%s_%s_view' % info),
        )
        return urlpatterns

    def has_change_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to change the given
        Django model instance.

        If `obj` is None, this should return True if the given request has
        permission to change *any* object of the given type.
        """
        change_all = super(FeedModelAdmin, self).has_change_permission(request, obj)
        return change_all or FeedAdminUtils.has_instance_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to change the given
        Django model instance.

        If `obj` is None, this should return True if the given request has
        permission to delete *any* object of the given type.
        """
        p=super(FeedModelAdmin, self).has_delete_permission(request, obj)

        if not p:
            if obj == None:
                return True
            else:
                return obj.created_by == request.user

        return p

    def get_view_formsets(self, request, obj=None):
        for view_inline in self.view_inline_instances:
            yield view_inline.get_formset(request, obj)

    def render_view_view(self, request, context, form_url='', obj=None):
        opts = self.model._meta
        app_label = opts.app_label
        context.update({
            'add': False,
            'change': False,
            'view': True,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'form_url': mark_safe(form_url),
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
            'root_path': reverse('admin:index'),
        })
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        if context.get('tabbed'):
            return render_to_response(self.view_form_template or [
                "admin/%s/%s/tabbed_view.html" % (app_label, opts.object_name.lower()),
                "admin/%s/tabbed_view.html" % app_label,
                "admin/tabbed_view.html"
            ], context, context_instance=context_instance)
        return render_to_response(self.view_form_template or [
                "admin/%s/%s/view.html" % (app_label, opts.object_name.lower()),
                "admin/%s/view.html" % app_label,
                "admin/view.html"
            ], context, context_instance=context_instance)

    def response_post_save_add(self, request, obj):
        """
        Return the appropriate response after adding an object. Called only if
        the "save" button clicked was not the "add another" or "continue"
        button.

        This means we have to handle our custom "save & next step" buttons
        here.
        """
        edit_url = reverse_lazy('admin:feed_%s_change' % type(obj).__name__.lower(), args=(obj.pk,))
        dest = self.get_redirect_destination(request, request.POST, obj, edit_url)
        # TODO: redirect to study overview page?
        return HttpResponseRedirect(dest)

    def response_post_save_change(self, request, obj):
        return self.response_post_save_add(request, obj)

    @csrf_protect_m
    def delete_view(self, *args, **kwargs):
        """
        Override ModelAdmin.delete_view() to augment template context with list
        of "critical" objects.  These are objects which should cause pause to
        deleters; the enforcement is in the template only and is not super
        secure.
        """

        res = super(FeedModelAdmin, self).delete_view(*args, **kwargs)

        # Add "associated critical objects" to context if possible.
        try:
            obj = res.context_data['object']
            res.context_data['associated_critical_objects'] = get_associated_critical_objects(obj)
        except AttributeError:
            # This exception will happen if res is an HttpResponseRedirect or
            # if context_data['object'] doesn't exist for some reason. In
            # either case, not much we can do.
            pass

        return res

    """
    get response url after deleting an object
    """
    def get_response_url(self,request):
        post_url = '../../'
        q_str = request.META['QUERY_STRING']
        if q_str in (None, ''):
            return post_url
        pos = q_str.find('created_by')
        if pos != -1:
            return "%s?%s" % (post_url, q_str)
        q_str= q_str.replace("=","/")
        return "../../../%s" % q_str

    """
    overwrite the function to set the created_by for any associated records before saving
    """
    def save_formset(self, request, form, formset, change):
        for f in formset.forms:
            if f.instance:
                if not f.instance.id:
                    f.instance.created_by = request.user


        formset.save()

    """
    overwrite the function to set the created_by for any associated records before saving
    """
    def save_form(self, request, form, change):
        if form.instance:
            if not form.instance.id:
                form.instance.created_by = request.user
        return form.save(commit=False)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        # Get default form values from session
        if add:
            request.feed_upload_status.apply_defaults_to_form(context['adminform'].form)
            context['clone_form'] = ModelCloneForm.factory(self, request)

        # Restrict values available in model select widgets based on session.
        #
        # First, apply to main form:
        request.feed_upload_status.apply_restricted_querysets_to_form(context['adminform'].form)

        # Second, apply to subforms (usually reverse FKs like channel lineups,
        # sensors, illustrations)
        for formset in context['inline_admin_formsets']:
            for form in formset.formset.forms:
                request.feed_upload_status.apply_restricted_querysets_to_form(form)

        if 'is_clone' in request.GET:
            if hasattr(obj, 'title'):
                context['adminform'].form.initial['title'] = ''
            elif hasattr(obj, 'name'):
                context['adminform'].form.initial['name'] = ''

        return super(FeedModelAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def clone_view(self, request, object_id, extra_context=None):
        "The 'clone' admin view for this model."

        exclude = [TrialInBucket, Illustration]
        model = self.model
        opts = model._meta
        app_label = opts.app_label

        try:
            obj = self.queryset(request).get(pk=unquote(object_id))
        except model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None

        if not self.has_add_permission(request):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if not obj.cloneable():
            message = "Not cloneable!"
            request.user.message_set.create(message=message)
            c = RequestContext(request, {})
            return render_to_response('error.html', c)

        cloned_obj = duplicate(obj,exclude)
        cloned_obj.save()

        msg = _('The %(name)s "%(obj)s" was cloned successfully. You may edit it now below.') % {'name': force_unicode(opts.verbose_name), 'obj': obj}
        self.message_user(request, msg)
        post_url="/admin/%s/%s/%d/edit" % (app_label, opts.object_name.lower(),cloned_obj.pk)
        if request.GET.has_key('r'):
            return_to = request.GET['r']
            if return_to !=None and return_to !="":
                post_url=return_to
        return HttpResponseRedirect(post_url)

    #overiten method to allow filtering in URL which is defaultly not allowed in 1.2.4
    def lookup_allowed(self, lookup, value):
        return True

    def change_view(self,request,object_id,extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        if obj is not None and self.has_change_permission(request, obj):
            request.feed_upload_status.update_with_object(obj, fail_silently=True)

        #add extra context for tabs
        if extra_context == None:
            extra_context = {}

        extra_context.update({
            'tabbed': self.tabbed,
            'tab_name': self.tab_name,
        })

        return super(FeedModelAdmin,self).change_view(request, object_id, extra_context=extra_context)

    #get context from the url if adding data
    def add_view(self, request, form_url='', extra_context=None):
        if extra_context == None:
            extra_context = {}

        if not request.method == 'POST':
            context_object = self.get_context(request)
            if context_object != None:
                context = {
                    'context_object': context_object,
                    'object_name': context_object.__class__.__name__,
                    'has_change_permission': self.has_change_permission(request, context_object),
                }
                extra_context.update(context)

        return super(FeedModelAdmin,self).add_view(request, form_url, extra_context)

    #get context object from the url parameter
    def get_context(self, request):

        v= request.GET.get("experiment")
        if v!=None:
            return Experiment.objects.get(pk = v)

        v= request.GET.get("emgsetup")
        if v!=None:
            return EmgSetup.objects.get(pk=v)

        v= request.GET.get("sonosetup")
        if v!=None:
            return SonoSetup.objects.get(pk=v)

        v= request.GET.get("strainsetup")
        if v!=None:
            return StrainSetup.objects.get(pk=v)

        v= request.GET.get("pressuresetup")
        if v!=None:
            return PressureSetup.objects.get(pk=v)

        v= request.GET.get("forcesetup")
        if v!=None:
            return ForceSetup.objects.get(pk=v)

        v= request.GET.get("kinematicssetup")
        if v!=None:
            return KinematicsSetup.objects.get(pk=v)
        v= request.GET.get("session")
        if v!=None:
            return Session.objects.get(pk=v)
        v= request.GET.get("study")
        if v!=None:
            return Study.objects.get(pk=v)

    def view_view(self, request, object_id, extra_context=None):
        "The 'View' admin view for this model."

        obj = self.get_object(request, unquote(object_id))
        if self.has_change_permission(request, obj):
            request.feed_upload_status.update_with_object(obj, fail_silently=True)

        model = self.model
        opts = model._meta

        try:
            obj = self.queryset(request).get(pk=unquote(object_id))
        except model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None

        #if not self.has_change_permission(request, obj):
        #    raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and request.POST.has_key("_saveasnew"):
            return self.add_view(request, form_url='../add/')

        ModelForm = self.get_form(request, obj)
        formsets = []

        form = ModelForm(instance=obj)

        prefixes = {}
        for FormSet in self.get_view_formsets(request, obj):
            prefix = FormSet.get_default_prefix()
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])
            formset = FormSet(instance=obj, prefix=prefix)
            formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj), self.prepopulated_fields)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.view_inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        registry = []
        for r in self.admin_site._registry:
            registry.append(r._meta.verbose_name.lower())

        context = {
            'title': _('View %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'cloneable': obj.cloneable(),
            'is_popup': request.REQUEST.has_key('_popup'),
            'tabbed': self.tabbed,
            'tab_name': self.tab_name,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': reverse('admin:index'),
            'app_label': opts.app_label,
            'registry': registry,
        }

        context.update(extra_context or {})
        return self.render_view_view(request, context, obj=obj)

    def changelist_view(self, request, extra_context=None):
        "The 'change list' admin view for this model."
        from feeddb.feed.extension.changelist import FeedChangeList
        opts = self.model._meta
        app_label = opts.app_label
        #if not self.has_change_permission(request, None):
        #    raise PermissionDenied
        # Check actions to see if any are available on this changelist
        actions = self.get_actions(request)
        # Remove action checkboxes if there aren't any actions available.
        list_display = list(self.list_display)
        if not actions:
            try:
                list_display.remove('action_checkbox')
            except ValueError:
                pass
        try:
            cl = FeedChangeList(request, self.model, list_display,
                self.list_display_links, self.list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related, self.list_per_page,
                self.list_max_show_all, self.list_editable, self)
        except IncorrectLookupParameters:
            # Wacky lookup parameters were given, so redirect to the main
            # changelist page, without parameters, and pass an 'invalid=1'
            # parameter via the query string. If wacky parameters were given and
            # the 'invalid=1' parameter was already in the query string, something
            # is screwed up with the database, so display an error page.
            if ERROR_FLAG in request.GET.keys():
                return render_to_response('admin/invalid_setup.html', {'title': _('Database error')})
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')
        # If the request was POSTed, this might be a bulk action or a bulk edit.
        # Try to look up an action first, but if this isn't an action the POST
        # will fall through to the bulk edit check, below.
        if actions and request.method == 'POST':
            response = self.response_action(request, queryset=cl.get_query_set())
            if response:
                return response
        # If we're allowing changelist editing, we need to construct a formset
        # for the changelist given all the fields to be edited. Then we'll
        # use the formset to validate/process POSTed data.
        formset = cl.formset = None
        # Handle POSTed bulk-edit data.
        if request.method == "POST" and self.list_editable:
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(request.POST, request.FILES, queryset=cl.result_list)
            if formset.is_valid():
                changecount = 0
                for form in formset.forms:
                    if form.has_changed():
                        obj = self.save_form(request, form, change=True)
                        self.save_model(request, obj, form, change=True)
                        form.save_m2m()
                        change_msg = self.construct_change_message(request, form, None)
                        self.log_change(request, obj, change_msg)
                        changecount += 1
                if changecount:
                    if changecount == 1:
                        name = force_unicode(opts.verbose_name)
                    else:
                        name = force_unicode(opts.verbose_name_plural)
                    msg = ungettext("%(count)s %(name)s was changed successfully.",
                                    "%(count)s %(name)s were changed successfully.",
                                    changecount) % {'count': changecount,
                                                    'name': name,
                                                    'obj': force_unicode(obj)}
                    self.message_user(request, msg)
                return HttpResponseRedirect(request.get_full_path())
        # Handle GET -- construct a formset for display.
        elif self.list_editable:
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(queryset=cl.result_list)
        # Build the list of media to be used by the formset.
        if formset:
            media = self.media + formset.media
        else:
            media = self.media
        # Build the action form and populate it with available actions.
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(request)
        else:
            action_form = None

        context = {
            'title': cl.title,
            'is_popup': cl.is_popup,
            'cl': cl,
            'media': media,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, None),
            'root_path': reverse('admin:index'),
            'app_label': app_label,
            'action_form': action_form,
            'actions_on_top': self.actions_on_top,
            'actions_on_bottom': self.actions_on_bottom,
            'change': False,
            'add': False,
            'view': True,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)



        return render_to_response(self.change_list_template or [
            'admin/%s/%s/change_list.html' % (app_label, opts.object_name.lower()),
            'admin/%s/change_list.html' % app_label,
            'admin/change_list.html'
        ], context, context_instance=context_instance)

class TermModelAdmin(FeedModelAdmin):
    change_list_template = "admin/term_change_list.html"

class FeedStackedInline(admin.StackedInline):
    template = 'admin/edit_inline/stacked.html'
    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs.pop("request", None)

        if db_field.choices:
            return self.formfield_for_choice_field(db_field, request, **kwargs)

        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            if db_field.__class__ in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[db_field.__class__], **kwargs)

            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)
            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(db_field, request, **kwargs)

            if formfield and db_field.name not in self.raw_id_fields:
                formfield.widget = FeedRelatedFieldWidgetWrapper(formfield.widget, db_field.rel, self.admin_site)

            return formfield

        for klass in db_field.__class__.mro():
            if klass in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[klass], **kwargs)
                return db_field.formfield(**kwargs)

        return db_field.formfield(**kwargs)

class DefaultModelAdmin(FeedModelAdmin):
    change_form_template = None

class SessionModelAdmin(FeedModelAdmin):
    def __init__(self, model, admin_site):
        super(SessionModelAdmin, self).__init__(model,admin_site)

    def get_urls(self):
        from django.conf.urls import patterns, url
        urls = super(SessionModelAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^edit/$',
                wrap(self.editlist_view),
                name='%s_%s_editlist' % info),
        )
        return urlpatterns+urls

    def editlist_view(self, request, extra_context=None):
        if request.GET.get("experiment") ==None:
            raise Http404("No experiment specified")

        model = Experiment
        object_id = request.GET.get("experiment")
        opts = model._meta

        try:
            obj = Experiment.objects.get(pk=unquote(object_id))
        except model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
        messages =[]
        errors =[]
        FormSet  = inlineformset_factory(Experiment, Session, SessionForm, PositionBaseInlineFormSet, can_delete=True)
        if request.method == 'POST':
            formsets=[]
            sessionformset = FormSet(request.POST, request.FILES, instance=obj )
            formsets.append(sessionformset)
            if all_valid(formsets):
                for f in sessionformset.forms:
                    if f.instance:
                        if not f.instance.id:
                            f.instance.created_by = request.user
                sessionformset.save()

                messages.append("Successfully updated the data!")
            else:
                errors.append(sessionformset.non_form_errors())
        else:
            sessionformset =FormSet(instance=obj)

        context={
            'experiment': obj,
            'object_id': object_id,
            'change': True,
            'add': False,
            'view': False,
            'sessionformset': sessionformset,
            'app_label': 'feed',
            'messages': messages,
        }
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response("admin/feed/session/edit_sessions.html", context, context_instance=context_instance)
    editlist_view = transaction.commit_on_success(editlist_view)

    def changelist_view(self, request, extra_context=None):
        experiment = None
        v= request.GET.get("experiment")
        if v!=None:
            experiment = Experiment.objects.get(pk = v)
        context = {
            'experiment': experiment,
            'has_change_permission': self.has_change_permission(request, experiment),
        }
        return super(SessionModelAdmin, self). changelist_view( request, context)

class EmgSensorModelAdmin(DefaultModelAdmin):
    def __init__(self, model, admin_site):
        super(EmgSensorModelAdmin, self).__init__(model,admin_site)

    def save_model(self, request, obj, form, change):
        form.save()
        try:
            emgchannel = EmgChannel.objects.get(sensor__id__exact = form.instance.id)
        except EmgChannel.DoesNotExist:
            emgchannel = EmgChannel()
            emgchannel.sensor=form.instance

        unit = request.POST['unit']
        filtering=request.POST['emg_filtering']
        amplification=request.POST['emg_amplification']
        rate=request.POST['rate']
        if unit!=None and unit!='':
            emgchannel.unit = Unit.objects.get(pk=int(unit))
        else:
            raise forms.ValidationError("Unit is required!")

        if filtering!=None and filtering!='':
            emgchannel.emg_filtering = Emgfiltering.objects.get(pk=int(filtering))
        else:
            raise forms.ValidationError("Emg Filtering is required!")

        if amplification!=None and amplification!='':
            emgchannel.emg_amplification = int(amplification)
        if rate!=None and rate!='':
	        emgchannel.rate = int(rate)
        emgchannel.name = form.instance.name
        emgchannel.setup = form.instance.setup
        emgchannel.save()

class EmgSetupModelAdmin(DefaultModelAdmin):
    def __init__(self, model, admin_site):
        super(EmgSetupModelAdmin, self).__init__(model,admin_site)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.id:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()
        if issubclass(formset.model,EmgSensor):
            for f in formset.forms:
	            for ins in instances:
	                if f.instance.id == ins.id:
	                    try:
	                        emgchannel = EmgChannel.objects.get(sensor__id__exact = ins.id)
	                    except EmgChannel.DoesNotExist:
	                        emgchannel = EmgChannel()
	                        emgchannel.sensor=ins

	                    unit = f.cleaned_data['unit']
	                    filtering=f.cleaned_data['emg_filtering']
	                    amplification=f.cleaned_data['emg_amplification']
	                    rate=f.cleaned_data['rate']
	                    if unit!=None and unit!='':
	                        emgchannel.unit = unit
	                    else:
	                        raise forms.ValidationError("Emg Unit is required!")

	                    if filtering!=None and filtering!='':
	                        emgchannel.emg_filtering = filtering
	                    else:
	                        raise forms.ValidationError("Emg Filtering is required!")

	                    if amplification!=None and amplification!='':
	                        emgchannel.emg_amplification = int(amplification)

	                    if rate!=None and rate!='':
	                        emgchannel.rate = int(rate)
	                    emgchannel.name = ins.name
	                    emgchannel.setup = ins.setup
	                    emgchannel.save()
