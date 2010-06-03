from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.encoding import force_unicode
from django.utils.translation import ungettext, ugettext as _
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.admin.util import _nest_help, get_change_view_url
from django.db.models.query import CollectedObjects
from django.db.models.fields.related import *

def get_feed_deleted_objects(deleted_objects, perms_needed, user, obj, opts, current_depth, admin_site, levels_to_root=4):
    """
    Helper function that recursively populates deleted_objects.

    `levels_to_root` defines the number of directories (../) to reach the
    admin root path. In a change_view this is 4, in a change_list view 2.

    This is for backwards compatibility since the options.delete_selected
    method uses this function also from a change_list view.
    This will not be used if we can reverse the URL.
    """
    nh = _nest_help # Bind to local variable for performance
    if current_depth > 16:
        return # Avoid recursing too deep.
    opts_seen = []
    for related in opts.get_all_related_objects():
        has_admin = related.model in admin_site._registry
        if related.opts in opts_seen:
            continue
        opts_seen.append(related.opts)
        rel_opts_name = related.get_accessor_name()
        if isinstance(related.field.rel, models.OneToOneRel):
            try:
                sub_obj = getattr(obj, rel_opts_name)
            except ObjectDoesNotExist:
                pass
            else:
                if has_admin:
                    p = '%s.%s' % (related.opts.app_label, related.opts.get_delete_permission())
                    if not user.has_perm(p):
                        if hasattr(obj,"created_by"):
                            if obj.created_by != user:
                                perms_needed.add(related.opts.verbose_name)
                                # We don't care about populating deleted_objects now.
                                continue
                if not has_admin:
                    # Don't display link to edit, because it either has no
                    # admin or is edited inline.
                    nh(deleted_objects, current_depth,
                        [u'%s: %s' % (capfirst(related.opts.verbose_name), force_unicode(sub_obj)), []])
                else:
                    # Display a link to the admin page.
                    nh(deleted_objects, current_depth, [mark_safe(u'%s: <a href="%s">%s</a>' %
                        (escape(capfirst(related.opts.verbose_name)),
                        get_change_view_url(related.opts.app_label,
                                            related.opts.object_name.lower(),
                                            sub_obj._get_pk_val(),
                                            admin_site,
                                            levels_to_root),
                        escape(sub_obj))), []])
                get_feed_deleted_objects(deleted_objects, perms_needed, user, sub_obj, related.opts, current_depth+2, admin_site)
        else:
            has_related_objs = False
            for sub_obj in getattr(obj, rel_opts_name).all():
                has_related_objs = True
                if not has_admin:
                    # Don't display link to edit, because it either has no
                    # admin or is edited inline.
                    nh(deleted_objects, current_depth,
                        [u'%s: %s' % (capfirst(related.opts.verbose_name), force_unicode(sub_obj)), []])
                else:
                    # Display a link to the admin page.
                    nh(deleted_objects, current_depth, [mark_safe(u'%s: <a href="%s">%s</a>' %
                        (escape(capfirst(related.opts.verbose_name)),
                        get_change_view_url(related.opts.app_label,
                                            related.opts.object_name.lower(),
                                            sub_obj._get_pk_val(),
                                            admin_site,
                                            levels_to_root),
                        escape(sub_obj))), []])
                get_feed_deleted_objects(deleted_objects, perms_needed, user, sub_obj, related.opts, current_depth+2, admin_site)
            # If there were related objects, and the user doesn't have
            # permission to delete them, add the missing perm to perms_needed.
            if has_admin and has_related_objs:
                p = '%s.%s' % (related.opts.app_label, related.opts.get_delete_permission())
                if not user.has_perm(p):
                    if hasattr(obj,"created_by"):
                        if obj.created_by != user:
                            perms_needed.add(related.opts.verbose_name)
    for related in opts.get_all_related_many_to_many_objects():
        has_admin = related.model in admin_site._registry
        if related.opts in opts_seen:
            continue
        opts_seen.append(related.opts)
        rel_opts_name = related.get_accessor_name()
        has_related_objs = False

        # related.get_accessor_name() could return None for symmetrical relationships
        if rel_opts_name:
            rel_objs = getattr(obj, rel_opts_name, None)
            if rel_objs:
                has_related_objs = True

        if has_related_objs:
            for sub_obj in rel_objs.all():
                if not has_admin:
                    # Don't display link to edit, because it either has no
                    # admin or is edited inline.
                    nh(deleted_objects, current_depth, [_('One or more %(fieldname)s in %(name)s: %(obj)s') % \
                        {'fieldname': force_unicode(related.field.verbose_name), 'name': force_unicode(related.opts.verbose_name), 'obj': escape(sub_obj)}, []])
                else:
                    # Display a link to the admin page.
                    nh(deleted_objects, current_depth, [
                        mark_safe((_('One or more %(fieldname)s in %(name)s:') % {'fieldname': escape(force_unicode(related.field.verbose_name)), 'name': escape(force_unicode(related.opts.verbose_name))}) + \
                        (u' <a href="%s">%s</a>' % \
                            (get_change_view_url(related.opts.app_label,
                                                 related.opts.object_name.lower(),
                                                 sub_obj._get_pk_val(),
                                                 admin_site,
                                                 levels_to_root),
                            escape(sub_obj)))), []])
        # If there were related objects, and the user doesn't have
        # permission to change them, add the missing perm to perms_needed.
        if has_admin and has_related_objs:
            p = u'%s.%s' % (related.opts.app_label, related.opts.get_change_permission())
            if not user.has_perm(p):
                if hasattr(obj,"created_by"):
                    if obj.created_by != user:
                        perms_needed.add(related.opts.verbose_name)
                        
def duplicate(obj, exclude = None, value=None, field=None):
    """
    Duplicate all related objects of `obj` setting
    `field` to `value`. If one of the duplicate
    objects has an FK to another duplicate object
    update that as well. Return the duplicate copy
    of `obj`.  
    """
       
    collected_objs = CollectedObjects()
    obj._collect_sub_objects(collected_objs)
    related_models = collected_objs.keys()
    root_obj = None
    # Traverse the related models in reverse deletion order.    
    for model in reversed(related_models):
        # Find all FKs on `model` that point to a `related_model`.
        
        fks = []
        for f in model._meta.fields:
            if isinstance(f, ForeignKey) and f.rel.to in related_models:
                fks.append(f)
        # Replace each `sub_obj` with a duplicate.
        sub_obj = collected_objs[model]
        for pk_val, obj in sub_obj.iteritems():
            if hasattr(obj,"clone"):
                obj= obj.clone(exclude)
            else:
                for fk in fks:
                    fk_value = getattr(obj, "%s_id" % fk.name)
                    # If this FK has been duplicated then point to the duplicate.
                    if fk_value in collected_objs[fk.rel.to]:
                        dupe_obj = collected_objs[fk.rel.to][fk_value]
                        setattr(obj, fk.name, dupe_obj)
            # Duplicate the object and save it.
            if exclude !=None:
                opts = obj._meta
                model_name = opts.object_name
                if not model_name in exclude:
                    obj.id = None
            else:
                obj.id = None

            if obj.id ==None:
                if hasattr(obj, 'name'):
                    setattr(obj,'name', "%s - cloned" % obj.name)
                if hasattr(obj, 'title'):
                    setattr(obj,'title', "%s - cloned" % obj.title)
            if field!=None and value!=None:
                setattr(obj, field, value)
            obj.save()
            if root_obj is None:
                root_obj = obj
    return root_obj
