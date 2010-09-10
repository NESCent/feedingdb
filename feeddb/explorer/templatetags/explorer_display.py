from django.template import Library
from django.conf import settings

register = Library()

def display_technique(trial):
    """
    Returns the unique techinique list for a trail.
    """
    techniques = set()
    
    for ch in trial.session.channels.all():
        if not ch.setup.technique.label in techniques:
            techniques.add(ch.setup.technique.label)
    return ','.join(techniques)
display_technique = register.simple_tag(display_technique)


def display_muscle(trial):
    """
    Returns the unique muscles list for a trail.
    """
    musles = set()
    
    for ch in trial.session.channels.all():
        for sensor in ch.setup.sensor_set.all():
            if hasattr(sensor, 'emgsensor') and  not sensor.emgsensor.location_controlled.label in musles:
                musles.add(sensor.emgsensor.location_controlled.label)
            if hasattr(sensor, 'sonosensor') and not sensor.sonosensor.location_controlled.label in musles:
                musles.add(sensor.sonosensor.location_controlled.label)
    return ','.join(musles)
display_muscle = register.simple_tag(display_muscle)

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
        return u'<a href="%s%s" title="click to view full size image"><img width="100" src="%s%s"/></a><br/>' % (settings.MEDIA_URL, value, settings.MEDIA_URL,value)

    return u'<a href="%s%s"><img src="%s%s" width="32"/></a><br/>' % (settings.MEDIA_URL,value, settings.STATIC_PREFIX, 'images/image-file-icon.png')
display_file = register.simple_tag(display_file)    