from django.template import Library
from django.conf import settings
from feeddb.feed.models import Techniques, EventChannel

#VG 2010-12-20 Most of the custom tags are the hack to look up descriptive strings from numeric codes,
#  to implement human-readable text in Explorer templates.
#  Properly, these should be supplied by the model, or looked up in forms, or looked up in
#  an intermediate layer of the application (yet to be architected...).

register = Library()

@register.simple_tag
def display_technique(trial):
    """
    Returns the unique technique list for a trial.
    """
    techn_ids = set()
    for ch in trial.session.channels.all():
        techn_ids.add(ch.setup.technique)
    techn_names = map(Techniques.num2label,  techn_ids)
    return ', '.join(techn_names)


@register.simple_tag
def technique_label(technique_num):
    return Techniques.num2label(technique_num)


def silent_if_none(x):
    """A helper function"""
    if x == None:  return ""
    else:          return unicode(x)

@register.simple_tag
def display_preamplifier(setup):
    if setup.technique == Techniques.ENUM.emg:
        return silent_if_none(setup.emgsetup.preamplifier)
    else:
        return ""

@register.simple_tag
def display_sonomicrometer(setup):
    if setup.technique == Techniques.ENUM.sono:
        return silent_if_none(setup.sonosetup.sonomicrometer)
    else:
        return ""

@register.simple_tag
def display_location(setup, sensor):
    return silent_if_none(sensor.get_location())

@register.simple_tag
def display_axisdepth(setup, sensor):
    if setup.technique == Techniques.ENUM.emg:
        return silent_if_none(sensor.emgsensor.axisdepth)
    elif setup.technique == Techniques.ENUM.sono:
        return silent_if_none(sensor.sonosensor.axisdepth)
    else:
        return ""

@register.simple_tag
def display_electrodetype(setup, sensor):
    if setup.technique == Techniques.ENUM.emg:
        return silent_if_none(sensor.emgsensor.electrode_type)
    else:
        return ""


@register.simple_tag
def display_unit(lineup):
    if lineup.channel.setup.technique == Techniques.ENUM.emg:
        return silent_if_none(lineup.channel.emgchannel.unit)
    elif lineup.channel.setup.technique == Techniques.ENUM.sono:
        return silent_if_none(lineup.channel.sonochannel.unit)
    elif lineup.channel.setup.technique == Techniques.ENUM.force:
        return silent_if_none(lineup.channel.forcechannel.unit)
    elif lineup.channel.setup.technique == Techniques.ENUM.kinematics:
        return silent_if_none(lineup.channel.kinematicschannel.unit)
    elif lineup.channel.setup.technique == Techniques.ENUM.pressure:
        return silent_if_none(lineup.channel.pressurechannel.unit)
    elif lineup.channel.setup.technique == Techniques.ENUM.strain:
        return silent_if_none(lineup.channel.strainchannel.unit)
    elif lineup.channel.setup.technique == Techniques.ENUM.event:
        return silent_if_none(lineup.channel.eventchannel.unit)
    elif lineup.channel.setup.technique == Techniques.ENUM.other:
        return "Unknown or N/A"
    else:
        return "ERROR: unknown technique in display_unit()"


@register.simple_tag
def display_sensor1(lineup):
    if lineup.channel.setup.technique == Techniques.ENUM.emg:
        return silent_if_none(lineup.channel.emgchannel.sensor.id)
    elif lineup.channel.setup.technique == Techniques.ENUM.sono:
        return silent_if_none(lineup.channel.sonochannel.crystal1.id)
    elif lineup.channel.setup.technique == Techniques.ENUM.force:
        return silent_if_none(lineup.channel.forcechannel.sensor.id)
    elif lineup.channel.setup.technique == Techniques.ENUM.kinematics:
        return silent_if_none(lineup.channel.kinematicschannel.sensor.id)
    elif lineup.channel.setup.technique == Techniques.ENUM.pressure:
        return silent_if_none(lineup.channel.pressurechannel.sensor.id)
    elif lineup.channel.setup.technique == Techniques.ENUM.strain:
        return silent_if_none(lineup.channel.strainchannel.sensor.id)
    elif lineup.channel.setup.technique == Techniques.ENUM.event:
        return ""
    elif lineup.channel.setup.technique == Techniques.ENUM.other:
        return silent_if_none(lineup.channel.otherchannel.sensor.id)
    else:
        return "ERROR: unknown technique in display_sensor1()"

@register.simple_tag
def display_sensor2(lineup):
    if lineup.channel.setup.technique == Techniques.ENUM.sono:
        return silent_if_none(lineup.channel.sonochannel.crystal2.id)
    else:
        return ""

@register.simple_tag
def display_emg_filtering(lineup):
    if lineup.channel.setup.technique == Techniques.ENUM.emg:
        return silent_if_none(lineup.channel.emgchannel.emg_filtering)
    else:
        return ""

@register.simple_tag
def display_emg_amplification(lineup):
    if lineup.channel.setup.technique == Techniques.ENUM.emg:
        return silent_if_none(lineup.channel.emgchannel.emg_amplification)
    else:
        return ""


@register.simple_tag
def display_lineup_location(lineup):
    channel = lineup.channel.typed()

    if type(channel) == EventChannel:
        return "N/A"

    # sonochannel
    try:
        loc1 = silent_if_none(channel.crystal1.get_location())
        loc2 = silent_if_none(channel.crystal2.get_location())
        return loc1 + u' : '  + loc2
    except AttributeError:
        pass

    # all other things
    try:
        return silent_if_none(channel.sensor.get_location())
    except AttributeError:
        pass


    return "ERROR: unknown technique in display_lineup_location()"

@register.simple_tag
def display_lineup_side(lineup):
    channel = lineup.channel.typed()

    # eventchannel
    if type(channel) == EventChannel:
        return "N/A"

    # sonochannel
    try:
        side1 = silent_if_none(channel.crystal1.loc_side)
        side2 = silent_if_none(channel.crystal2.loc_side)
        return side1 + " : " + side2
    except AttributeError:
        pass

    # all other things
    try:
        return silent_if_none(channel.sensor.loc_side)
    except AttributeError:
        pass


    return "ERROR: unknown technique in display_lineup_location()"

def is_image(file):
    """
    Check if the file is a image based on the extension
    """
    img_exts = [".jpeg",".png",".gif",".jpg",".bmp"]
    for ext in img_exts:

        if file.url.lower().find(ext) !=-1:
            return True
    return False

def display_file(value):
    """
    If file is an image display <img> tag with the file as src, otherwise display <a> link with file as href
    """
    if value in (None, ''):
        return ""
    if is_image(value):
        return u'<a href="%s%s" title="click to view full size image" class="thumb"><img width="100" src="%s%s"/></a><br/>' % (settings.MEDIA_URL, value, settings.MEDIA_URL,value)

    return u'<a href="%s%s"><span class="glyphicon glyphicon-picture">' % (settings.MEDIA_URL,value,)
display_file = register.simple_tag(display_file)
