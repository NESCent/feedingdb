from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.contrib.admin.views.main import ALL_VAR, EMPTY_CHANGELIST_VALUE
from django.contrib.admin.views.main import ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import formats
from django.utils.html import escape, conditional_escape
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.template import Library
from feeddb.explorer.templatetags.explorer_display import display_file
import datetime

register = Library()

def feed_result_headers(cl):
    lookup_opts = cl.lookup_opts

    for i, field_name in enumerate(cl.list_display):
        attr = None
        try:
            f = lookup_opts.get_field(field_name)
            admin_order_field = None
        except models.FieldDoesNotExist:
            # For non-field list_display values, check for the function
            # attribute "short_description". If that doesn't exist, fall back
            # to the method name. And __str__ and __unicode__ are special-cases.
            if field_name == '__unicode__':
                header = force_unicode(lookup_opts.verbose_name)
            elif field_name == '__str__':
                header = smart_str(lookup_opts.verbose_name)
            else:
                if callable(field_name):
                    attr = field_name # field_name can be a callable
                else:
                    try:
                        attr = getattr(cl.model_admin, field_name)
                    except AttributeError:
                        try:
                            attr = getattr(cl.model, field_name)
                        except AttributeError:
                            raise AttributeError, \
                                "'%s' model or '%s' objects have no attribute '%s'" % \
                                    (lookup_opts.object_name, cl.model_admin.__class__, field_name)

                try:
                    header = attr.short_description
                except AttributeError:
                    if callable(field_name):
                        header = field_name.__name__
                    else:
                        header = field_name
                    header = header.replace('_', ' ')

            # It is a non-field, but perhaps one that is sortable
            admin_order_field = getattr(attr, "admin_order_field", None)
            if not admin_order_field:
                yield {"text": header}
                continue

            # So this _is_ a sortable non-field.  Go to the yield
            # after the else clause.
        else:
            header = f.verbose_name

        th_classes = []
        new_order_type = 'asc'

        # FIXME: throws error "'FeedChangeList' object has no attribute 'order_field'"
        #if field_name == cl.order_field or admin_order_field == cl.order_field:
        #    th_classes.append('sorted %sending' % cl.order_type.lower())
        #    new_order_type = {'asc': 'desc', 'desc': 'asc'}[cl.order_type.lower()]

        yield {"text": header,
               "sortable": True,
               "url": cl.get_query_string({ORDER_VAR: i, ORDER_TYPE_VAR: new_order_type}),
               "class_attrib": mark_safe(th_classes and ' class="%s"' % ' '.join(th_classes) or '')}

def _boolean_icon(field_val):
    BOOLEAN_MAPPING = {True: 'ok-sign', False: 'minus-sign', None: 'question-sign'}
    
    return mark_safe(u'<span class="glyphicon glyphicon-%s"></span>' % ( BOOLEAN_MAPPING[field_val], ))
        

def feed_items_for_result(cl, result, form):
    first = True
    pk = cl.lookup_opts.pk.attname
    for field_name in cl.list_display:
        row_class = ''
        try:
            f = cl.lookup_opts.get_field(field_name)
        except models.FieldDoesNotExist:
            # For non-field list_display values, the value is either a method,
            # property or returned via a callable.
            try:
                if callable(field_name):
                    attr = field_name
                    value = attr(result)
                elif hasattr(cl.model_admin, field_name) and \
                   not field_name == '__str__' and not field_name == '__unicode__':
                    attr = getattr(cl.model_admin, field_name)
                    value = attr(result)
                else:
                    attr = getattr(result, field_name)
                    if callable(attr):
                        value = attr()
                    else:
                        value = attr
                allow_tags = getattr(attr, 'allow_tags', False)
                boolean = getattr(attr, 'boolean', False)
                if boolean:
                    allow_tags = True
                    result_repr = _boolean_icon(value)
                else:
                    result_repr = smart_unicode(value)
            except (AttributeError, ObjectDoesNotExist):
                result_repr = EMPTY_CHANGELIST_VALUE
            else:
                # Strip HTML tags in the resulting text, except if the
                # function has an "allow_tags" attribute set to True.
                if not allow_tags:
                    result_repr = escape(result_repr)
                else:
                    result_repr = mark_safe(result_repr)
        else:
            field_val = getattr(result, f.attname)

            if isinstance(f.rel, models.ManyToOneRel):
                if field_val is not None:
                    result_repr = escape(getattr(result, f.name))
                else:
                    result_repr = EMPTY_CHANGELIST_VALUE
            # Dates and times are special: They're formatted in a certain way.
            elif isinstance(f, models.DateField) or isinstance(f, models.TimeField):
                if field_val:
                    if isinstance(f, models.DateTimeField):
                        result_repr = capfirst(formats.date_format(field_val, 'DATETIME_FORMAT'))
                    elif isinstance(f, models.TimeField):
                        result_repr = capfirst(formats.time_format(field_val))
                    else:
                        result_repr = capfirst(formats.date_format(field_val))
                else:
                    result_repr = EMPTY_CHANGELIST_VALUE
                row_class = ' class="nowrap"'
            # Booleans are special: We use images.
            elif isinstance(f, models.BooleanField) or isinstance(f, models.NullBooleanField):
                result_repr = _boolean_icon(field_val)
            # DecimalFields are special: Zero-pad the decimals.
            elif isinstance(f, models.DecimalField):
                if field_val is not None:
                    result_repr = ('%%.%sf' % f.decimal_places) % field_val
                else:
                    result_repr = EMPTY_CHANGELIST_VALUE
            # Fields with choices are special: Use the representation
            # of the choice.
            elif f.flatchoices:
                result_repr = dict(f.flatchoices).get(field_val, EMPTY_CHANGELIST_VALUE)
            #file fields
            elif isinstance(f, models.FileField):
                result_repr = mark_safe(display_file(field_val))
            else:
                result_repr = escape(field_val)
        if force_unicode(result_repr) == '':
            result_repr = mark_safe('&nbsp;')

        if form and field_name in form.fields:
            bf = form[field_name]
            result_repr = mark_safe(force_unicode(bf.errors) + force_unicode(bf))
        else:
            result_repr = conditional_escape(result_repr)
        yield mark_safe(u'<td%s>%s</td>' % (row_class, result_repr))
    if form:
        yield mark_safe(force_unicode(form[cl.model._meta.pk.name]))

def feed_results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield list(feed_items_for_result(cl, res, form))
    else:
        for res in cl.result_list:
            lst= list(feed_items_for_result(cl, res, None))
            name_args = (cl.opts.app_label, cl.opts.model_name)
            try:
                view_url = reverse('admin:%s_%s_view' % name_args, args=(res.pk,))
                view_anchor = "<span class='glyphicon glyphicon-eye-open' alt='%s'></span>" % settings.STATIC_PREFIX
                view_action = u'<a href="%s">%s</a>' % (view_url, view_anchor)
            except NoReverseMatch:
                view_action = ''

            try:
                change_url = reverse('admin:%s_%s_change' % name_args, args=(res.pk,))
                if hasattr(cl, "request"):
                    if cl.request.META['QUERY_STRING']:
                        change_url = '%s?%s' % (change_url, cl.request.META['QUERY_STRING'])

                change_anchor = "<span class='glyphicon glyphicon-pencil' alt='%s'></span>" % settings.STATIC_PREFIX
                change_action = u'<a href="%s">%s</a>' % (change_url, change_anchor)
            except NoReverseMatch:
                change_action = ''

            try:
                delete_url = reverse('admin:%s_%s_delete' % name_args, args=(res.pk,))
                if hasattr(cl, "request"):
                    qd = cl.request.GET.copy()
                    if not 'cancel' in qd:
                        qd['cancel'] = cl.request.get_full_path()
                    if not 'next' in qd:
                        qd['next'] = cl.request.get_full_path()

                    delete_url = '%s?%s' % (delete_url, qd.urlencode(safe='/'))

                delete_anchor = "<span class='glyphicon glyphicon-remove' alt='%s'></span>" % settings.STATIC_PREFIX
                delete_action = u'<a href="%s">%s</a>' % (delete_url, delete_anchor)
            except NoReverseMatch:
                delete_action = ''

            try:
                clone_url = reverse('admin:%s_%s_clone' % name_args, args=(res.pk,))
                clone_anchor = "<span class='glyphicon glyphicon-plus-sign' alt='%s'></span>" % settings.STATIC_PREFIX
                clone_action = u'<a href="%s">%s</a>' % (clone_url, clone_anchor)
            except NoReverseMatch:
                clone_action = ''

            if hasattr(cl, "request"):
                if cl.model_admin.has_change_permission (cl.request, res):
                    view_action = u'%s%s'  % (view_action, change_action)
                if cl.model_admin.has_delete_permission (cl.request, res):
                    view_action = u'%s%s'  % (view_action, delete_action)
                if cl.model_admin.has_change_permission (cl.request, res):
                    try:
                        if cl.model.is_cloneable:
                            view_action = u'%s%s'  % (view_action, clone_action)
                    except AttributeError:
                        pass

            lst.append(mark_safe(u'<td class="action">%s</td>' % view_action))
            yield lst

@register.inclusion_tag("admin/change_list_results.html", takes_context=True)
def feed_result_list(context, cl):
    if not hasattr(cl, 'request') and 'request' in context:
        cl.request = context['request']
    header_list = list(feed_result_headers(cl))
    act =   {"text": "action",
               "sortable": False,
               "url": "",
               "class_attrib": mark_safe(" class='action_header'")}

    header_list.append(act)
    return {'cl': cl,
            'result_headers': header_list,
            'results': list(feed_results(cl))}
