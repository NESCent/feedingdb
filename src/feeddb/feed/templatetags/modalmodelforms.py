from django import template
from django.db.models.loading import get_model
from django.core.urlresolvers import NoReverseMatch, reverse
from django.conf import settings

register = template.Library()

@register.inclusion_tag('modalmodelforms/modal_add_link.html')
def modal_add_link(boundfield, url=None, app='feed'):
    try:
        field = boundfield.field
        model = field.queryset.model
        modelname = model.__name__.lower()
    except AttributeError:
        raise ValueError("Could not find a model for the given BoundField instance. The tag {% modal_add_link <boundfield> %} can only work with ModelChoiceField objects which provide a queryset")

    if url is None:
        try:
            url = reverse('modal_add_' + modelname)
        except NoReverseMatch as e:
            raise ValueError("Could not find modal form URL for model '%s'" % modelname, e)

    return {
        'url': url,
        'modelname': modelname,
        'select_element_id': boundfield.id_for_label,
        'boundfield': boundfield,
        'DEBUG': settings.DEBUG,
    }
