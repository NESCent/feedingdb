from django.template import Library

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