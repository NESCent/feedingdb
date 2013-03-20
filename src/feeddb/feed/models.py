from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime
from django.db.models.expressions import F


DATETIME_HELP_TEXT = 'For older dates, type by hand "yyyy-mm-dd" for date and "hh:mm:ss" for time, for example "1990-10-22" and "15:45:00.  If start time is not known, use "00:00:00".' 
# Only used for Trial here; the other containers are are affected through forms.py -- go figure (VG) 
BOOKKEEPING_HELP_TEXT = 'The reference to these data, as used in your lab notes or records (optional).'

class FeedBaseModel(models.Model):
    """Base model for the whole project """
    created_by = models.ForeignKey(User, related_name="%(class)s_related", editable=False,  blank=True, null=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    is_cloneable = False
    
    class Meta:
        abstract = True

    def cloneable(self):
        return self.is_cloneable
        
    def save(self):
        now = datetime.datetime.today()
        if not self.id:
            self.created_at = now
        self.updated_at = now
        super(FeedBaseModel, self).save()

#cvterms
class CvTerm(FeedBaseModel):
    label = models.CharField(max_length=255)
    is_cloneable = False
    
    def __unicode__(self):
        return self.label
    class Meta:
        ordering = ["label"]
        abstract = True
       
class DevelopmentStage(CvTerm):
    pass

class AgeUnit(CvTerm):
    pass

    
    
TECHNIQUE_CHOICES = (
               (1, u'EMG'),
               (2, u'Sono'), 
               (3, u'Strain'), 
               (4, u'Bite force'), 
               (5, u'Pressure'), 
               (6, u'Kinematics'), 
               (7, u'Time/Event'), 
               )
    
class Techniques(object):
    CHOICES = TECHNIQUE_CHOICES
    __choices_dict = dict(TECHNIQUE_CHOICES)

    class ENUM:
        emg = 1
        sono = 2
        strain = 3
        force = 4 
        pressure = 5 
        kinematics = 6
        event = 7
        
    @staticmethod
    def num2label(num):
        return Techniques.__choices_dict.get(num, "Unknown Technique")


class Taxon(CvTerm):
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, blank = True, null=True)
    def __unicode__(self):
        return "%s %s (%s)" % (self.genus, self.species, self.common_name)
#        return self.genus+" "+ self.species + " ()"
    class Meta:
        ordering = ["genus"]
        verbose_name_plural = "Taxa"


class AnatomicalCategories:     # An "enumeration", not a Django model
    muscle = 1
    bone = 2

ANATOMICAL_CATEGORIES = (
        (AnatomicalCategories.muscle, u'Muscle'), 
        (AnatomicalCategories.bone, u'Bone')
                                  )
class AnatomicalLocation(CvTerm):
    category = models.IntegerField(choices=ANATOMICAL_CATEGORIES)


class Side(CvTerm):
    pass

class DepthAxis(CvTerm):
    class Meta:
        verbose_name = "depth point"
        verbose_name_plural = "depth axis"


class AnteriorPosteriorAxis(CvTerm):
    class Meta:
        verbose_name = "anterior-posterior point"
        verbose_name_plural = "anterior-posterior axis"


class DorsalVentralAxis(CvTerm):
    class Meta:
        verbose_name = "dorsal-ventral point"
        verbose_name_plural = "dorsal-ventral axis"

class ProximalDistalAxis(CvTerm):
    class Meta:
        verbose_name = "proximal-distal point"
        verbose_name_plural = "proximal-distal axis"
        
class MedialLateralAxis(CvTerm):
    class Meta: 
        verbose_name = "medial-lateral point"
        verbose_name_plural = "medial-lateral axis"


class ElectrodeType(CvTerm):
    pass

class Behavior(CvTerm):
    pass

class Restraint(CvTerm):
    pass


class Unit(CvTerm):
    technique  = models.IntegerField(choices = Techniques.CHOICES)   
    
    class Meta:
        ordering = ["technique", "label"]


class Emgfiltering(CvTerm):
    pass

#object models    
class Study(FeedBaseModel):
    accession = models.CharField(max_length=255, blank = True, null=True)
    title = models.CharField(max_length=255, 
                             help_text = "A descriptive name of this study.")
    bookkeeping = models.CharField("Bookkeeping",max_length=255, blank = True, null=True, help_text = BOOKKEEPING_HELP_TEXT)
    start = models.DateTimeField(blank = False, null=False)
    end = models.DateTimeField( blank = True, null=True)
    funding_agency = models.CharField(max_length=255, blank = True, null=True)
    approval_secured = models.CharField(max_length=255, blank = True, null=True, 
                                        help_text = "Whether an approval for Animal Care and Use or for Human Subjects was secured (Yes, No, or N/A).")
    description = models.TextField()
    resources = models.TextField("External Resources", blank = True, null=True)

    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Studies"
    
class StudyPrivate(FeedBaseModel):
    study = models.ForeignKey(Study)
    pi = models.CharField("PI", max_length=255)
    organization = models.CharField(max_length=255, blank = True, null=True)
    lab = models.CharField(max_length=255, blank = True, null=True)
    funding = models.CharField(max_length=255, blank = True, null=True, help_text = "Funding agency, grant name, number, award date, etc.")
    approval = models.CharField(max_length=255, blank = True, null=True, 
                                help_text = "A reference to approval documentation for Animal Care and Use or for Human Subjects, if it was secured.")
    notes = models.TextField( blank = True, null=True)
    class Meta:
        verbose_name = "Study - Private Information"
        verbose_name_plural = "Study - Private Information"
'''
'''
class Subject(FeedBaseModel):
    is_cloneable = False
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    
    study = models.ForeignKey(Study)
    taxon = models.ForeignKey(Taxon)
    name = models.CharField(max_length=255)    
    breed = models.CharField(max_length=255, blank = True, null=True)   
    sex = models.CharField(max_length=2, choices = GENDER_CHOICES, blank = True, null=True) 
    source = models.CharField(max_length=255, blank = True, null=True, 
                              help_text = "E.g. wild-caught, zoo, laboratory raised, etc.")
    notes = models.TextField(blank = True, null=True, help_text="E.g., any relevant morphological data, such as muscle weights, muscle fiber angles, fiber types, CT scan images, anatomical drawings.")
    def __unicode__(self):
        return self.name       
        
class Experiment(FeedBaseModel):
    accession = models.CharField(max_length=255, blank = True, null=True)
    title = models.CharField(max_length=255)
    bookkeeping = models.CharField("bookkeeping", max_length=255,blank = True, null=True, help_text = BOOKKEEPING_HELP_TEXT)
    study = models.ForeignKey(Study)    
    subject = models.ForeignKey(Subject)   
    start = models.DateTimeField( blank = True, null=True)
    end = models.DateTimeField(blank = True, null=True)
    description = models.TextField(blank = True, null=True)
    subj_devstage = models.ForeignKey(DevelopmentStage,verbose_name="subject development stage")
    subj_age = models.DecimalField("subject age",max_digits=19, decimal_places=5, blank = True, null=True, 
                                   help_text = "As a decimal; use the following field to specify age units.")
    subj_ageunit = models.ForeignKey(AgeUnit, verbose_name='age units', blank = True, null = True)
    subj_weight = models.DecimalField("subject weight (kg)",max_digits=19, decimal_places=5, blank = True, null=True)
    subj_tooth = models.CharField("subject teeth",max_length=255, blank = True, null=True, 
                                  help_text = "Stage of teeth development")
    subject_notes = models.TextField("subject notes", blank = True, null=True)
    impl_notes = models.TextField("implantation notes", blank = True, null=True)
    def __unicode__(self):
        return self.title

class Setup(FeedBaseModel):
    is_cloneable=False
    experiment = models.ForeignKey(Experiment)
    technique = models.IntegerField(choices=Techniques.CHOICES)   
    notes = models.TextField("Notes about all sensors and channels in this setup", blank = True, null=True)
    sampling_rate = models.IntegerField("Sampling Rate (Hz)", blank=True, null=True)
    class Meta:
        verbose_name = "setup"
    def __unicode__(self):
        return "%s setup" % (Techniques.num2label(self.technique))  

class EmgSetup(Setup):
    preamplifier = models.CharField(max_length=255, blank = True, null=True)
    class Meta:
        verbose_name = "EMG setup"
    def __unicode__(self):
        return "%s setup" % (Techniques.num2label(self.technique))  

class SonoSetup(Setup):
    sonomicrometer = models.CharField(max_length=255, blank = True, null=True)
    class Meta:
        verbose_name = "Sono setup"

class StrainSetup(Setup):
    class Meta:
        verbose_name = "Strain setup"
        
class ForceSetup(Setup):
    class Meta:
        verbose_name = "Bite Force setup" 

class PressureSetup(Setup):
    class Meta:
        verbose_name = "Pressure setup" 

class KinematicsSetup(Setup):
    class Meta:
        verbose_name = "Kinematics setup" 

    def save(self):
        if self.notes in (None, '') and self.id == None:
            self.notes = 'camera\nmarkers\nmovie film or digital\nlight or x-ray\nanatomical view (lateral/d-v/frontal)\n2D or 3D'
        super(KinematicsSetup, self).save()

class EventSetup(Setup):    
    class Meta:
        verbose_name = "Time/Event setup"
        
        
class Sensor(FeedBaseModel):
    setup = models.ForeignKey(Setup)
    name = models.CharField(max_length=255)

    location_freetext = models.CharField("Anatomical Location (free text)", max_length=255, blank = True, null=True)
    #location_controlled  -- a companion field in some Sensor subclasses
    
    loc_side = models.ForeignKey(Side, verbose_name="Side", null=False)   
    loc_ap = models.ForeignKey(AnteriorPosteriorAxis, verbose_name="AP", blank = True, null=True )
    loc_dv = models.ForeignKey(DorsalVentralAxis, verbose_name="DV", blank = True, null=True )
    loc_pd = models.ForeignKey(ProximalDistalAxis, verbose_name="PD", blank = True, null=True )
    loc_ml = models.ForeignKey(MedialLateralAxis, verbose_name="ML", blank = True, null=True ) 
    
    notes = models.TextField( blank = True, null=True)
    def __unicode__(self):
        return self.name  

class EmgSensor(Sensor):    
    location_controlled = models.ForeignKey(AnatomicalLocation, verbose_name = "Muscle", null=False,    
                                            limit_choices_to = {'category__exact' : AnatomicalCategories.muscle}) 
    
    axisdepth = models.ForeignKey(DepthAxis, verbose_name="Electrode depth", blank = True, null=True )
    electrode_type = models.ForeignKey(ElectrodeType,
        verbose_name="Electrode type", blank = True, null=True )

    def __unicode__(self):
        return 'EMG Sensor: %s (Muscle: %s, Side: %s) '  % (self.name, self.location_controlled.label, self.loc_side.label)  

    class Meta:
        verbose_name = "EMG electrode"
        ordering = ["id"]

class SonoSensor(Sensor):
    location_controlled = models.ForeignKey(AnatomicalLocation, verbose_name = "Muscle", null=False,    
                                            limit_choices_to = {'category__exact' : AnatomicalCategories.muscle}) 

    axisdepth = models.ForeignKey(DepthAxis, verbose_name="Crystal depth", blank = True, null=True )
    def __unicode__(self):
        return self.name  

    class Meta:
        verbose_name = "Sono crystal"

class StrainSensor(Sensor):
    class Meta:
        verbose_name = "Strain sensor"
    
class ForceSensor(Sensor):
    class Meta:
        verbose_name = "Bite Force sensor"
    
class PressureSensor(Sensor):
    class Meta:
        verbose_name = "Pressure sensor"
    
class KinematicsSensor(Sensor):
    class Meta:
        verbose_name = "Kinematics marker"

    
class Channel(FeedBaseModel):
    setup = models.ForeignKey(Setup)
    name = models.CharField(max_length = 255)
    rate = models.IntegerField("Recording Rate (Hz)")
    notes = models.TextField("Notes",  blank = True, null=True)

    def __unicode__(self):
        return self.name 

class EmgChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.emg},
                             verbose_name="EMG units [from models.py]")     
    sensor = models.ForeignKey(EmgSensor)    
    emg_filtering = models.ForeignKey(Emgfiltering, verbose_name="EMG filtering")
    emg_amplification = models.IntegerField(blank=True,null=True,verbose_name = "amplification")
    
    def __unicode__(self):
        return 'EMG Channel: %s (Muscle: %s, Side: %s) '  % (self.name, self.sensor.location_controlled.label, self.sensor.loc_side.label)  
    class Meta:
        verbose_name = "EMG channel"


class SonoChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.sono},
                             verbose_name="Sono units")     
    crystal1 = models.ForeignKey(SonoSensor, related_name="crystals1_related")
    crystal2 = models.ForeignKey(SonoSensor, related_name="crystals2_related")

    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = "Sono channel"

class StrainChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.strain},
                             verbose_name="Strain units", null=True) 
    sensor = models.ForeignKey(StrainSensor)
    class Meta:
        verbose_name = "Strain channel"

class ForceChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.force},
                             verbose_name="Bite Force units", null=True) 
    sensor = models.ForeignKey(ForceSensor)
    class Meta:
        verbose_name = "Bite Force channel"
               
class PressureChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.pressure},
                             verbose_name="Pressure units", null=True) 
    sensor = models.ForeignKey(PressureSensor)
    class Meta:
        verbose_name = "Pressure channel"
               
class KinematicsChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.kinematics},
                             verbose_name="Kinematics units", null=True) 
    sensor = models.ForeignKey(KinematicsSensor, verbose_name="Marker")
    class Meta:
        verbose_name = "Kinematics channel"
              
class EventChannel(Channel):
    unit = models.CharField(max_length=255, blank = True, null = True)
    #Note: An EventChannel is not associated with any Sensor
    class Meta:
        verbose_name = "Time/Event channel" 
    
              
class Session(FeedBaseModel):
    accession = models.CharField(max_length=255, blank = True, null=True)
    title = models.CharField(max_length=255)
    bookkeeping = models.CharField("bookkeeping", max_length=255,blank = True, null=True, help_text = BOOKKEEPING_HELP_TEXT)
    experiment = models.ForeignKey(Experiment)    
    position = models.IntegerField(help_text='The numeric position of this recording session among the other sessions within the current experiment.')
    start = models.DateTimeField(blank = True, null=True)
    end = models.DateTimeField(blank = True, null=True)
    subj_notes = models.TextField("subject notes", blank = True, null=True)    
    subj_restraint = models.ForeignKey(Restraint,verbose_name="subject restraint")
    subj_anesthesia_sedation = models.CharField("subject anesthesia / sedation", max_length=255,  blank = True, null=True)
    
    channels  = models.ManyToManyField(Channel, through='ChannelLineup')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["position"]


# function to decide the upload_to for trial data file
# upload_to = [media_root]/data/study_[study id]/experiment_[experiment id]/session_[session id]
def get_data_upload_to(instance, filename):
    session=instance.session
    experiment = session.experiment
    study = experiment.study
    return 'data/study_%d/experiment_%d/session_%d/%s' % (study.id, experiment.id,session.id, filename)

class Trial(FeedBaseModel):
    accession = models.CharField(max_length=255, blank = True, null=True)
    title = models.CharField(max_length=255)
    bookkeeping = models.CharField("bookkeeping", max_length=255,blank = True, null=True, help_text = BOOKKEEPING_HELP_TEXT)
    session = models.ForeignKey(Session)    
    position = models.IntegerField(help_text='The numeric position of this trial among the other trials within the current recording session.')
    start = models.DateTimeField( blank = True, null=True, help_text = DATETIME_HELP_TEXT)
    end = models.DateTimeField(blank = True, null=True, help_text = DATETIME_HELP_TEXT)
    estimated_duration = models.PositiveIntegerField("Estimated duration (sec)", blank = True, null=True) 
    subj_treatment = models.TextField("subject treatment",blank = True, null=True)
    subj_notes = models.TextField("subject notes", blank = True, null=True)

    food_type = models.CharField("food type", max_length=255,blank = True, null=True)
    food_size = models.CharField("Food size (maximum dimension millimeters)", max_length=255,blank = True, null=True)
    food_property = models.CharField("food property", max_length=255,blank = True, null=True)

    behavior_primary = models.ForeignKey(Behavior,verbose_name="primary behavior")
    behavior_secondary = models.CharField("secondary behavior", max_length=255,blank = True, null=True)
    behavior_notes = models.TextField("behavior notes", blank = True, null=True)

    data_file  = models.FileField("Data File",upload_to=get_data_upload_to ,  blank = True, null=True, 
                                  help_text="A tab-delimited file with columns corresponding to the channel lineup specified in the Recording Session.")
    waveform_picture = models.FileField("waveform picture",upload_to="pictures",  blank = True, null=True, 
                                        help_text="A picture (jpeg, pdf, etc.) as a graphical overview of data in the data file.")

    def __unicode__(self):
        return self.title          
    def taxon_name(self):
        return self.session.experiment.subject.taxon.label
    taxon_name.short_description = 'Species'

class Illustration(FeedBaseModel):
    picture = models.FileField("picture",upload_to='illustrations',  blank = True, null=True)
    notes = models.TextField(blank = True, null=True)
    #A hack: It is intended that only one of the following FKs is non-null.  
    subject  = models.ForeignKey(Subject,  blank = True, null=True)
    setup  = models.ForeignKey(Setup,  blank = True, null=True)
    experiment  = models.ForeignKey(Experiment,  blank = True, null=True)
    
class ChannelLineup(FeedBaseModel):
    session = models.ForeignKey(Session)
    position = models.IntegerField(help_text='The numeric position of the channel within this channel lineup; coincides with the column position in the data file.')
    channel = models.ForeignKey(Channel, null=True, blank=True)

    class Meta:
        ordering = ["position"]
        verbose_name = "Channel Position"
        verbose_name_plural = "Channel Lineup"
    def __unicode__(self):
        return str(self.position)
        
"""
CRITICAL_ASSOCIATED_OBJECTS stores critical associated objects in model level for determine if an object can be deleted. 
The policy is that only object that has no associated critical objects can be deleted.
"""
        
CRITICAL_ASSOCIATED_OBJECTS = {}
CRITICAL_ASSOCIATED_OBJECTS[Channel]=['session_set']
CRITICAL_ASSOCIATED_OBJECTS[Session]=['channellineup_set']
CRITICAL_ASSOCIATED_OBJECTS[Unit]=['emgchannel_set','sonochannel_set','strainchannel_set','forcechannel_set','pressurechannel_set','kinematicschannel_set']
CRITICAL_ASSOCIATED_OBJECTS[Taxon]=['subject_set']
CRITICAL_ASSOCIATED_OBJECTS[DevelopmentStage]=['experiment_set']
CRITICAL_ASSOCIATED_OBJECTS[AgeUnit]=['experiment_set']
CRITICAL_ASSOCIATED_OBJECTS[AnatomicalLocation]=['emgsensor_set','sonosensor_set']
CRITICAL_ASSOCIATED_OBJECTS[DepthAxis]=['emgsensor_set','sonosensor_set']
CRITICAL_ASSOCIATED_OBJECTS[Side]=['sensor_set']
CRITICAL_ASSOCIATED_OBJECTS[AnteriorPosteriorAxis]=['sensor_set']
CRITICAL_ASSOCIATED_OBJECTS[DorsalVentralAxis]=['sensor_set']
CRITICAL_ASSOCIATED_OBJECTS[ProximalDistalAxis]=['sensor_set']
CRITICAL_ASSOCIATED_OBJECTS[MedialLateralAxis]=['sensor_set']
CRITICAL_ASSOCIATED_OBJECTS[ElectrodeType]=['emgsensor_set']
CRITICAL_ASSOCIATED_OBJECTS[Behavior]=['trial_set']
CRITICAL_ASSOCIATED_OBJECTS[Restraint]=['session_set']
CRITICAL_ASSOCIATED_OBJECTS[Emgfiltering]=['emgchannel_set']
CRITICAL_ASSOCIATED_OBJECTS[Subject]=['experiment_set']
