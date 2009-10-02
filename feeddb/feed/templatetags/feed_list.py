from django.conf import settings
from django.contrib.admin.views.main import ALL_VAR, EMPTY_CHANGELIST_VALUE
from django.contrib.admin.views.main import ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import dateformat
from django.utils.html import escape, conditional_escape
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.utils.translation import get_date_formats, get_partial_date_formats, ugettext as _
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.template import Library
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
        if field_name == cl.order_field or admin_order_field == cl.order_field:
            th_classes.append('sorted %sending' % cl.order_type.lower())
            new_order_type = {'asc': 'desc', 'desc': 'asc'}[cl.order_type.lower()]

        yield {"text": header,
               "sortable": True,
               "url": cl.get_query_string({ORDER_VAR: i, ORDER_TYPE_VAR: new_order_type}),
               "class_attrib": mark_safe(th_classes and ' class="%s"' % ' '.join(th_classes) or '')}

def _boolean_icon(field_val):
    BOOLEAN_MAPPING = {True: 'yes', False: 'no', None: 'unknown'}
    return mark_safe(u'<img src="%simg/admin/icon-%s.gif" alt="%s" />' % (settings.ADMIN_MEDIA_PREFIX, BOOLEAN_MAPPING[field_val], field_val))

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
                    (date_format, datetime_format, time_format) = get_date_formats()
                    if isinstance(f, models.DateTimeField):
                        result_repr = capfirst(dateformat.format(field_val, datetime_format))
                    elif isinstance(f, models.TimeField):
                        result_repr = capfirst(dateformat.time_format(field_val, time_format))
                    else:
                        result_repr = capfirst(dateformat.format(field_val, date_format))
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
            view_url = cl.url_for_result(res)
            change_url = "%sedit" % view_url
            delete_url = "%sdelete" % view_url
            if hasattr(cl, "request"):
                if cl.request.META['QUERY_STRING']:  
                    change_url = '%s/?%s' % (change_url, cl.request.META['QUERY_STRING'])
                    delete_url = '%s/?%s' % (delete_url, cl.request.META['QUERY_STRING'])
            view_anchor = "<img src='/media/img/admin/icon_calendar.gif' alt='view' title='view'/>"
            change_anchor = "<img src='/media/img/admin/icon_changelink.gif' alt='edit' title='edit'/>"
            delete_anchor = "<img src='/media/img/admin/icon_deletelink.gif' alt='delete' title='delete' />"
            '''
            view_action = u'<li><a href="%s">%s</a></li>' % (view_url, view_anchor)
            change_action = u'<li><a href="%s">%s</a></li>' % (change_url, change_anchor)
            delete_action = u'<li><a href="%s">%s</a></li>' % (delete_url, delete_anchor)
            '''
            view_action = u'<a href="%s">%s</a>' % (view_url, view_anchor)
            change_action = u'<a href="%s">%s</a>' % (change_url, change_anchor)
            delete_action = u'<a href="%s">%s</a>' % (delete_url, delete_anchor)
            if hasattr(cl, "request"):
                if cl.model_admin.has_change_permission (cl.request, res):
                    view_action = u'%s%s'  % (view_action, change_action)
                if cl.model_admin.has_delete_permission (cl.request, res):
                    view_action = u'%s%s'  % (view_action, delete_action)		
            #lst.append(mark_safe(u'<td class="action"><ul class="feed-object-tools">%s</ul></td>' % view_action))
            lst.append(mark_safe(u'<td class="action">%s</td>' % view_action))
            yield lst

def feed_result_list(cl):
    header_list = list(feed_result_headers(cl))
    act =   {"text": "action",
               "sortable": False,
               "url": "",
               "class_attrib": mark_safe(" class='action_header'")}

    header_list.append(act)
    return {'cl': cl,
            'result_headers': header_list,
            'results': list(feed_results(cl))}
feed_result_list = register.inclusion_tag("admin/change_list_results.html")(feed_result_list)
