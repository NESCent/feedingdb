from django.contrib import admin
from django import forms, template
from django.forms.formsets import all_valid
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import widgets
from django.contrib.admin import helpers
from django.contrib.admin.util import unquote, flatten_fieldsets, model_ngettext, model_format_dict
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.db.models.fields import BLANK_CHOICE_DASH
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.datastructures import SortedDict
from django.utils.functional import update_wrapper
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.functional import curry
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext, ugettext_lazy
from django.utils.encoding import force_unicode
from feeddb.feed.models import  *
from feeddb.feed.extension.widgets import FeedRelatedFieldWidgetWrapper
from feeddb.feed.extension.forms import *
from feeddb.feed.extension.formsets import PositionBaseInlineFormSet
from django.forms.util import ValidationError
from feeddb.feed.extension.changelist import *
from feeddb.feed.extension.util import get_feed_deleted_objects

class FeedTabularInline(admin.TabularInline):
    template = 'admin/edit_inline/tabular.html'
    change_form_template = 'admin/tabbed_change_form.html'
    tabbed = False
    tab_name = None

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

class FeedModelAdmin(admin.ModelAdmin):
    view_inlines = []

    # Custom templates (designed to be over-ridden in subclasses)
    view_form_template = None

    # Actions
    actions = None

    # tabbed view?
    tabbed = False
    tab_name = None

    def __init__(self, model, admin_site):
        super(FeedModelAdmin, self).__init__(model,admin_site)
        self.view_inline_instances = []
        for view_inline_class in self.view_inlines:
            view_inline_instance = view_inline_class(self.model, self.admin_site)
            self.view_inline_instances.append(view_inline_instance)

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

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
        p=super(FeedModelAdmin, self).has_change_permission(request, obj)
        
        if not p:
            if obj == None:
                return True
            return obj.created_by == request.user
        
        return p 

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
        ordered_objects = opts.get_ordered_objects()
        context.update({
            'add': False,
            'change': False,
            'view': True, 
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'ordered_objects': ordered_objects,
            'form_url': mark_safe(form_url),
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
            'root_path': self.admin_site.root_path,
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

    def response_add(self, request, obj, post_url_continue='../%s/edit/'):
        """
        Determines the HttpResponse for the add_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            rel_obj=None
            rel_obj_id = None
            for k in request.GET:
                rel_obj = k
                rel_obj_id = request.GET[k]
            if rel_obj != None and rel_obj!="created_by":
                post_url = '../../%s/%s' % (rel_obj, rel_obj_id)
            elif self.has_change_permission(request, None):
                post_url = '../'
            else:
                post_url = '../../../'
            return HttpResponseRedirect(post_url)

    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        try:
            obj = self.queryset(request).get(pk=unquote(object_id))
        except self.model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        deleted_objects = [mark_safe(u'%s: <a href="../../%s/">%s</a>' % (escape(force_unicode(capfirst(opts.verbose_name))), object_id, escape(obj))), []]
        perms_needed = set()
        get_feed_deleted_objects(deleted_objects, perms_needed, request.user, obj, opts, 1, self.admin_site)

        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_unicode(obj)
            self.log_deletion(request, obj, obj_display)
            obj.delete()

            self.message_user(request, _('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})

            post_url = '../../'
            rel_obj = None 
            for k in request.GET:
                rel_obj = k
                rel_obj_id = request.GET.get(k)
            if rel_obj != None and rel_obj!="created_by":
                post_url = '/admin/feed/%s/%s' % (rel_obj, rel_obj_id)
            if hasattr(obj,'experiment'):
                post_url='/admin/feed/experiment/%s' % obj.experiment.pk
            return HttpResponseRedirect(post_url)

        context = {
            "title": _("Are you sure?"),
            "object_name": force_unicode(opts.verbose_name),
            "object": obj,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "opts": opts,
            "root_path": self.admin_site.root_path,
            "app_label": app_label,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, context_instance=context_instance)

    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.REQUEST.has_key('_popup'):
                return HttpResponseRedirect(request.path + "?_popup=1")
            else:
                return HttpResponseRedirect(request.path)
        elif request.POST.has_key("_saveasnew"):
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % {'name': force_unicode(opts.verbose_name), 'obj': obj}
            self.message_user(request, msg)
            return HttpResponseRedirect("../%s/" % pk_value)
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect("../add/")
        else:
            rel_obj=None
            rel_obj_id = None
            for k in request.GET:
                rel_obj = k
                rel_obj_id = request.GET[k]
            if rel_obj != None and rel_obj!="created_by":
                post_url = '../../../%s/%s' % (rel_obj, rel_obj_id)
            else:
                post_url = request.path
            self.message_user(request, msg)
            return HttpResponseRedirect(post_url)

    """
    overwrite the function to set the created_by for any associated records before saving

    """ 
    def save_formset(self, request, form, formset, change):
        for f in formset.forms:
            if f.instance:
                f.instance.created_by = request.user

        
        formset.save()

    """
    overwrite the function to set the created_by for any associated records before saving

    """  
    def save_form(self, request, form, change):
        if form.instance:
            form.instance.created_by = request.user
        return form.save(commit=False)

 
    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        if request.method == 'POST':
            return super(FeedModelAdmin,self).add_view(request, form_url, extra_context)
        
        model = self.model
        opts = model._meta
        
        if not self.has_add_permission(request):
            raise PermissionDenied
 
        ModelForm = self.get_form(request)
        formsets = []
        
        # Prepare the dict of initial data from the request.
        # We have to special-case M2Ms as a list of comma-separated PKs.
        initial = dict(request.GET.items())
        for k in initial:
            try:
                f = opts.get_field(k)
            except models.FieldDoesNotExist:
                continue
            if isinstance(f, models.ManyToManyField):
                initial[k] = initial[k].split(",")
        form = ModelForm(initial=initial)
            
        #filtering choices
        self.filter_form_values(request, form,model,None)
        
        prefixes = {}
        for FormSet in self.get_formsets(request):
            prefix = FormSet.get_default_prefix()
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])
            formset = FormSet(instance=self.model(), prefix=prefix)
            formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)), self.prepopulated_fields)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            self.filter_formset_values(request,formset,model,None)
            fieldsets = list(inline.get_fieldsets(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': request.REQUEST.has_key('_popup'),
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)
    add_view = transaction.commit_on_success(add_view)

    def change_view(self, request, object_id, extra_context=None):
        "The 'change' admin view for this model."
        if request.method == 'POST':
            return super(FeedModelAdmin, self).change_view(request, object_id, extra_context)
        
        model = self.model
        opts = model._meta

        try:
            obj = self.queryset(request).get(pk=unquote(object_id))
        except model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None
        
        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        
        ModelForm = self.get_form(request, obj)
        formsets = []
        
        form = ModelForm(instance=obj)
        #filtering choices
        self.filter_form_values(request, form,model,obj)
        prefixes = {}
        for FormSet in self.get_formsets(request, obj):
            prefix = FormSet.get_default_prefix()
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])
            formset = FormSet(instance=obj, prefix=prefix)
            formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj), self.prepopulated_fields)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            self.filter_formset_values(request,formset,model,obj)
            fieldsets = list(inline.get_fieldsets(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
            
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        active_tab_name = self.tab_name
        for fs in inline_admin_formsets:
            error_count = 0
            for err in fs.formset.errors: 
                if err: error_count = error_count+1
            for err in fs.formset.non_form_errors(): 
                if err: error_count = error_count+1

            if error_count>0:
                if fs.opts.tab_name: 
                    active_tab_name = fs.opts.tab_name
                else:
                    active_tab_name = fs.opts.verbose_name


        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'tabbed': self.tabbed,
            'tab_name': self.tab_name,
            'active_tab_name': active_tab_name,
            'is_popup': request.REQUEST.has_key('_popup'),
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)
    change_view = transaction.commit_on_success(change_view)
    
    def filter_form_values(self, request, form, model, obj):
        #globally disabled the accession field
        if form.fields.has_key("accession"):
            form.fields["accession"].widget.attrs['disabled']=""

        #general set all choices from the user own data
        if not request.user.is_superuser:
            if form.fields.has_key("study"):
                form.fields["study"].queryset = Study.objects.filter(created_by=request.user)
            if form.fields.has_key("experiment"):
                form.fields["experiment"].queryset = Experiment.objects.filter(created_by=request.user)
            if form.fields.has_key("subject"):
                form.fields["subject"].queryset = Subject.objects.filter(created_by=request.user)
            if form.fields.has_key("setup"):
                form.fields["setup"].queryset = Setup.objects.filter(created_by=request.user)
            if form.fields.has_key("emgsetup"):
                form.fields["emgsetup"].queryset = EmgSetup.objects.filter(created_by=request.user)
            if form.fields.has_key("sonosetup"):
                form.fields["sonosetup"].queryset = SonoSetup.objects.filter(created_by=request.user)
            if form.fields.has_key("channel"):
                form.fields["channel"].queryset = Channel.objects.filter(created_by=request.user)
            if form.fields.has_key("emgchannel"):
                form.fields["emgchannel"].queryset = EmgChannel.objects.filter(created_by=request.user)
            if form.fields.has_key("sonochannel"):
                form.fields["sonochannel"].queryset = SonoChannel.objects.filter(created_by=request.user)
            if form.fields.has_key("session"):
                form.fields["session"].queryset = Session.objects.filter(created_by=request.user)
            if form.fields.has_key("trial"):
                form.fields["trial"].queryset = Trial.objects.filter(created_by=request.user)

        #disable corresponding foriegn key select box if the data object is already specified in the url
        if request.GET.has_key("study"):
            if form.fields.has_key("study"):
                form.fields["study"].widget.widget.attrs['disabled']=""
        if request.GET.has_key("experiment"):
            if form.fields.has_key("experiment"):
                form.fields["experiment"].widget.widget.attrs['disabled']=""

        if request.GET.has_key("subject"):
            if form.fields.has_key("subject"):
                form.fields["subject"].widget.widget.attrs['disabled']=""

        if request.GET.has_key("emgsetup"):
            if form.fields.has_key("setup"):
                form.fields["setup"].widget.widget.attrs['disabled']=""

        if request.GET.has_key("sonosetup"):
            if form.fields.has_key("setup"):
                form.fields["setup"].widget.widget.attrs['disabled']=""

        if request.GET.has_key("session"):
            if form.fields.has_key("session"):
                form.fields["session"].widget.widget.attrs['disabled']=""

        if request.GET.has_key("trial"):
            if form.fields.has_key("trial"):
                form.fields["trial"].widget.widget.attrs['disabled']=""

        if request.GET.has_key("emgchannel"):
            if form.fields.has_key("emgchannel"):
                form.fields["emgchannel"].widget.widget.attrs['disabled']=""
        if request.GET.has_key("sonochannel"):
            if form.fields.has_key("sonochannel"):
                form.fields["sonochannel"].widget.widget.attrs['disabled']=""
        #context-based filter
        if  model == EmgChannel:
            if request.GET.has_key("emgsetup"):
                form.fields["sensor"].queryset = EmgSensor.objects.filter(setup=request.GET['emgsetup'])
                form.fields["setup"].initial=request.GET['emgsetup']
        elif  model == Experiment:
            if form.fields.has_key("subject") and obj:
                form.fields["subject"].queryset = Subject.objects.filter(study=obj.study)
        elif  model == EmgElectrode:
            if request.GET.has_key("emgsetup"):
                form.fields["setup"].initial=request.GET['emgsetup']
        elif  model == Illustration:
            if request.GET.has_key("emgsetup"):
                form.fields["setup"].initial=request.GET['emgsetup']
            if request.GET.has_key("sonosetup"):
                form.fields["setup"].initial=request.GET['sonosetup']
            if request.GET.has_key("subject"):
                form.fields["subject"].initial=request.GET['subject']
        elif  model == SonoChannel:
            if request.GET.has_key("sonosetup"):
                form.fields["crystal1"].queryset = SonoSensor.objects.filter(setup=request.GET['sonosetup'])
                form.fields["crystal2"].queryset = SonoSensor.objects.filter(setup=request.GET['sonosetup'])
                form.fields["setup"].initial=request.GET['sonosetup']
        elif model == SonoSetup:
            if form.fields.has_key("crystal1"):
                form.fields["crystal1"].queryset = SonoSensor.objects.filter(setup=obj)
                form.fields["crystal2"].queryset = SonoSensor.objects.filter(setup=obj)
        elif  model == EmgSensor:
            if request.GET.has_key("emgsetup"):
                form.fields["setup"].initial=request.GET['emgsetup']
        elif  model == SonoSensor:
            if request.GET.has_key("sonosetup"):
                form.fields["setup"].initial=request.GET['sonosetup']
            else:
                pass
        elif  model == Session:
            if obj !=None and form.fields.has_key("channel"): 
                form.fields["channel"].queryset = Channel.objects.filter(setup__experiment = obj.experiment.id)
            elif request.GET.has_key("experiment") and form.fields.has_key("channel"): 
                form.fields["channel"].queryset = Channel.objects.filter(setup__experiment=request.GET['experiment'])
        elif  model == ChannelLineup:
            if request.GET.has_key("session") and form.fields.has_key("channel"): 
                sess = Session.objects.get(id=  request.GET['session'])
                form.fields["channel"].queryset = Channel.objects.filter(setup__experiment=sess.experiment.id)

    def filter_formset_values(self, request, formset, model, obj):
        for form in formset.forms:
            self.filter_form_values(request, form, model, obj)
    
    def view_view(self, request, object_id, extra_context=None):
        "The 'View' admin view for this model."
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
            'is_popup': request.REQUEST.has_key('_popup'),
            'tabbed': self.tabbed,
            'tab_name': self.tab_name,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
            'registry': registry,
        }
        
        context.update(extra_context or {})
        return self.render_view_view(request, context, obj=obj)
    
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
            cl = FeedChangeList(request, self.model, list_display, self.list_display_links, self.list_filter,
                self.date_hierarchy, self.search_fields, self.list_select_related, self.list_per_page, self.list_editable, self)
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
            'root_path': self.admin_site.root_path,
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

class ExperimentModelAdmin(FeedModelAdmin):
    def __init__(self, model, admin_site):
        super(ExperimentModelAdmin, self).__init__(model,admin_site)

    def change_view(self, request, object_id, extra_context=None):
        model = self.model
        opts = model._meta

        try:
            obj = self.queryset(request).get(pk=unquote(object_id))
        except model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None
        
        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        response = super(ExperimentModelAdmin, self).change_view(request, object_id, extra_context)
        if request.method != 'POST':
            return response

        self.add_techniques(request,obj)
        return response 

    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta
        
        if not self.has_add_permission(request):
            raise PermissionDenied
 
        ModelForm = self.get_form(request)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            form.created_by_id = request.user.pk
            
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=False)
                new_object.created_by = request.user
                
            else:
                form_validated = False
                new_object = self.model()
            prefixes = {}
            for FormSet in self.get_formsets(request):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=new_object,
                                  save_as_new=request.POST.has_key("_saveasnew"),
                                  prefix=prefix)
                formsets.append(formset)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=False)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset( request, form, formset, change=False)
                self.log_addition(request, new_object)
                self.add_techniques(request,new_object)
                return self.response_add(request, new_object)
        return super(ExperimentModelAdmin,self).add_view(request, form_url,extra_context)
    
    def add_techniques(self, request, new_experiment):
        "handle techniques for this experiment."
        #FIXME: consider refactoring this into a series of calls to technique-generic functions, to eliminate code repetition
        has_emg = False
        emgsetup = None
        has_sono = False
        sonosetup=None
        has_strain = False
        strainsetup=None
        has_force = False
        forcesetup=None
        has_pressure=False
        pressuresetup=None
        has_kinematics=False
        kinematicssetup=None
        
        for s in new_experiment.setup_set.all():
            if hasattr(s,"emgsetup"):
                has_emg = True
                emgsetup = s
            if hasattr(s, "sonosetup"):
                has_sono = True
                sonosetup = s
            if hasattr(s, "strainsetup"):
                has_strain = True
                strainsetup = s
            if hasattr(s, "forcesetup"):
                has_force = True
                forcesetup = s  
            if hasattr(s, "pressuresetup"):
                has_pressure = True
                pressuresetup = s       
            if hasattr(s, "kinematicssetup"):
                has_kinematics = True
                kinematicssetup = s               
        emg  = request.POST.get('technique_emg')
        
        if emg != None and emg == "on":
            if not has_emg:
                self.add_technique(request,new_experiment,'EMG');
        if emg == None and has_emg:
            self.delete_setup(emgsetup)
            
        sono  = request.POST.get('technique_sono')
        if sono != None and sono == "on":
            if not has_sono:
                self.add_technique(request,new_experiment,'Sono');
        if sono == None and has_sono: 
            self.delete_setup(sonosetup)
            
        strain  = request.POST.get('technique_strain')
        if strain != None and strain == "on":
            if not has_strain:
                self.add_technique(request,new_experiment,'Bone strain');
        if strain == None and has_strain: 
            self.delete_setup(strainsetup)
        
        force  = request.POST.get('technique_force')
        if force != None and force == "on":
            if not has_force:
                self.add_technique(request,new_experiment,'Bite force');
        if force == None and has_force: 
            self.delete_setup(forcesetup)
        
        pressure  = request.POST.get('technique_pressure')
        if pressure != None and pressure == "on":
            if not has_pressure:
                self.add_technique(request,new_experiment,'Pressure');
        if pressure == None and has_pressure: 
            self.delete_setup(pressuresetup)        
        
        kinematics  = request.POST.get('technique_kinematics')
        if kinematics != None and kinematics == "on":
            if not has_kinematics:
                self.add_technique(request,new_experiment,'Kinematics');
        if kinematics == None and has_kinematics: 
            self.delete_setup(kinematicssetup)                  

    def add_technique(self,request,experiment, technique):
        tech = Technique.objects.get(label = technique)
        setup = Setup();
        setup.technique=tech
        setup.experiment = experiment
        tech_setup = None
        if technique=="EMG":
            tech_setup = EmgSetup()
        elif technique=="Sono":
            tech_setup = SonoSetup()
        elif technique=="Bone strain":
            tech_setup = StrainSetup()
        elif technique=="Bite force":
            tech_setup = ForceSetup()
        elif technique=="Pressure":
            tech_setup = PressureSetup()
        elif technique=="Kinematics":
            tech_setup = KinematicsSetup()
            
        tech_setup.experiment = experiment
        tech_setup.technique=tech
        if technique=="EMG":
            setup.emgsetup = tech_setup
        elif technique=="Sono":
            setup.sonosetup = tech_setup
        elif technique=="Bone strain":
            setup.strainsetup = tech_setup
        elif technique=="Bite force":
            setup.forcesetup = tech_setup    
        elif technique=="Kinematics":
            setup.kinematicssetup = tech_setup  
        elif technique=="Pressure":
            setup.pressuresetup = tech_setup  
        tech_setup.created_by = request.user

        setup.created_by = request.user
        tech_setup.save()
    
    def delete_setup(self,setup):
        if setup!=None:
            if hasattr(setup,"setup"):
                setup.setup.delete()
            setup.delete()
            
    def changelist_view(self, request, extra_context=None):
        experiment = None
        v= request.GET.get("experiment")
        if v!=None:
            experiment = Experiment.objects.get(pk = v) 
        context = {
            'experiment': experiment,
            'has_change_permission': self.has_change_permission(request, experiment),
        }
        return super(ExperimentModelAdmin, self). changelist_view( request, context)

class SessionModelAdmin(FeedModelAdmin):
    def __init__(self, model, admin_site):
        super(SessionModelAdmin, self).__init__(model,admin_site)

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^edit/$',
                wrap(self.editlist_view),
                name='%s_%s_editlist' % info),
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
            url(r'^(.+)/$',
                wrap(self.view_view),
                name='%s_%s_view' % info),
        )
        return urlpatterns

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
        if request.method == 'POST':
            formsets=[]
            FormSet  = inlineformset_factory(Experiment, Session, SessionForm, PositionBaseInlineFormSet, can_delete=True)
            sessionformset = FormSet(request.POST, request.FILES, instance=obj )
            formsets.append(sessionformset)
            if all_valid(formsets):
                for f in sessionformset.forms:
                    if f.instance:
                        f.instance.created_by = request.user
                sessionformset.save()

                messages.append("Successfully updated the data!")
            else:
                errors.append(sessionformset.non_form_errors())
            form = SessionForm(instance=obj)
            
            context={
                    'experiment': obj,
                    'object_id': object_id,
                     'change': True,
                     'add': False,
                     'view': False,
                     'sessionformset': sessionformset,
                     'app_label': 'feed',
                     'messages': messages,
                     'errors': errors,
            }
            context_instance = template.RequestContext(request, current_app=self.admin_site.name)
            return render_to_response("admin/feed/session/edit_sessions.html", context, context_instance=context_instance)
        else:
            form = SessionForm(instance=obj)
            FormSet  = inlineformset_factory(Experiment, Session, SessionForm, PositionBaseInlineFormSet, can_delete=True)
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
