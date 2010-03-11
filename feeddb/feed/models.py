from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime


# base model for the whole project

class FeedBaseModel(models.Model):
    created_by = models.ForeignKey(User, related_name="%(class)s_related", editable=False,  blank=True, null=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
   
    class Meta:
        abstract = True

    def save(self):
        now = datetime.datetime.today()
        if not self.id:
            self.created_at = now
        self.updated_at = now
        super(FeedBaseModel, self).save()

#cvterms
class CvTerm(FeedBaseModel):
    label = models.CharField(max_length=255)
    controlled = models.BooleanField()
    deprecated = models.BooleanField()
    def __unicode__(self):
        return self.label
    class Meta:
        ordering = ["label"]
        abstract = True

class DevelopmentStage(CvTerm):
    pass

class Technique(CvTerm):
    pass

class Taxon(CvTerm):
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, blank = True, null=True)
    def __unicode__(self):
        return self.genus+" "+ self.species 
    class Meta:
        ordering = ["genus"]
        verbose_name_plural = "Taxa"

class Muscle(CvTerm):
    pass

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


class ElectrodeType(CvTerm):
    pass

class Behavior(CvTerm):
    pass

class Restraint(CvTerm):
    pass

class Emgunit(CvTerm):
    pass

class Sonounit(CvTerm):
    pass

class Emgfiltering(CvTerm):
    pass

#object models    
class Study(FeedBaseModel):
    accession = models.CharField(max_length=255, blank = True, null=True)
    title = models.CharField(max_length=255)
    bookkeeping = models.CharField("Bookkeeping",max_length=255, blank = True, null=True)
    start = models.DateTimeField(blank = True, null=True, help_text='format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00')
    end = models.DateTimeField( blank = True, null=True, help_text='format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00')
    funding_agency = models.CharField(max_length=255, blank = True, null=True)
    approval_secured = models.CharField(max_length=255, blank = True, null=True)
    description = models.TextField()

    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Studies"
    
class StudyPrivate(FeedBaseModel):
    study = models.ForeignKey(Study)
    pi = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank = True, null=True)
    lab = models.CharField(max_length=255, blank = True, null=True)
    funding = models.CharField(max_length=255, blank = True, null=True)
    approval = models.CharField(max_length=255, blank = True, null=True)
    notes = models.TextField( blank = True, null=True)
    class Meta:
        verbose_name = "Study - Private Information"
        verbose_name_plural = "Study - Private Information"
'''
'''
class Subject(FeedBaseModel):
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    
    study = models.ForeignKey(Study)
    taxon = models.ForeignKey(Taxon)
    name = models.CharField(max_length=255)    
    breed = models.CharField(max_length=255, blank = True, null=True)   
    sex = models.CharField(max_length=2, choices = GENDER_CHOICES, blank = True, null=True) 
    source = models.CharField(max_length=255, blank = True, null=True) 
    notes = models.TextField(blank = True, null=True, help_text="notes about the research subject")
    def __unicode__(self):
        return self.name       
        
class Experiment(FeedBaseModel):
    accession = models.CharField(max_length=255, blank = True, null=True)
    title = models.CharField(max_length=255, default="new Experiment - edit this")
    bookkeeping = models.CharField("bookkeeping", max_length=255,blank = True, null=True)
    study = models.ForeignKey(Study)    
    subject = models.ForeignKey(Subject)   
    start = models.DateTimeField( blank = True, null=True, help_text='format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00')
    end = models.DateTimeField(blank = True, null=True, help_text='format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00')
    description = models.TextField()
    subj_devstage = models.ForeignKey(DevelopmentStage,verbose_name="subject development stage")
    subj_age = models.DecimalField("subject age",max_digits=19, decimal_places=5, blank = True, null=True)
    subj_weight = models.DecimalField("subject weight",max_digits=19, decimal_places=5, blank = True, null=True)
    subj_tooth = models.CharField("subject teeth",max_length=255, blank = True, null=True)
    subject_notes = models.TextField("subject notes", blank = True, null=True)
    impl_notes = models.TextField("implantation notes", blank = True, null=True)
    def __unicode__(self):
        return self.title

class Setup(FeedBaseModel):
    experiment = models.ForeignKey(Experiment)
    technique = models.ForeignKey(Technique)     
    notes = models.TextField("Notes about all sensors and channels in this setup", blank = True, null=True)
    class Meta:
        verbose_name = "setup"
    def __unicode__(self):
        return "%s setup" % (self.technique)  

class EmgSetup(Setup):
    preamplifier = models.CharField(max_length=255, blank = True, null=True)
    class Meta:
        verbose_name = "EMG setup"
    def __unicode__(self):
        return "%s setup with preamplifier: %s" % (self.technique, self.preamplifier)  

class SonoSetup(Setup):
    sonomicrometer = models.CharField(max_length=255, blank = True, null=True)
    class Meta:
        verbose_name = "Sono setup"
    def __unicode__(self):
        return "%s setup with sonomicrometer: %s" % (self.technique, self.sonomicrometer)  

class Sensor(FeedBaseModel):
    setup = models.ForeignKey(Setup)
    name = models.CharField(max_length=255)
    notes = models.TextField( blank = True, null=True)
    def __unicode__(self):
        return self.name  

class EmgSensor(Sensor):
    muscle = models.ForeignKey(Muscle)
    side = models.ForeignKey(Side, verbose_name="side of muscle" )
    axisdepth = models.ForeignKey(DepthAxis, verbose_name="depth point", blank = True, null=True )
    axisap = models.ForeignKey(AnteriorPosteriorAxis, verbose_name="anterior-posterior point", blank = True, null=True )
    axisdv = models.ForeignKey(DorsalVentralAxis, verbose_name="dorsal-ventral point", blank = True, null=True )
    electrode_type = models.ForeignKey(ElectrodeType,
        verbose_name="electrode type", blank = True, null=True )

    def __unicode__(self):
        return 'EMG Sensor: %s (Muscle: %s, Side: %s) '  % (self.name, self.muscle.label, self.side.label)  

    class Meta:
        verbose_name = "EMG sensor"
        ordering = ["id"]

class SonoSensor(Sensor):
    muscle = models.ForeignKey(Muscle )
    side = models.ForeignKey(Side, verbose_name="side of muscle" )
    axisdepth = models.ForeignKey(DepthAxis, verbose_name="depth point", blank = True, null=True )
    axisap = models.ForeignKey(AnteriorPosteriorAxis, verbose_name="anterior-posterior point", blank = True, null=True )
    axisdv = models.ForeignKey(DorsalVentralAxis, verbose_name="dorsal-ventral point", blank = True, null=True )
    def __unicode__(self):
        return 'Sono Sensor: %s (Muscle: %s, Side: %s) '  % (self.name, self.muscle.label, self.side.label)  

    class Meta:
        verbose_name = "Sono sensor"
    
class Channel(FeedBaseModel):
    setup = models.ForeignKey(Setup)
    name = models.CharField(max_length = 255)
    rate = models.IntegerField()
    notes = models.TextField("Notes about the channel",  blank = True, null=True)

    def __unicode__(self):
        return self.name 

class EmgChannel(Channel):
    sensor = models.ForeignKey(EmgSensor)    
    emg_unit = models.ForeignKey(Emgunit, verbose_name="EMG units")
    emg_filtering = models.ForeignKey(Emgfiltering, verbose_name="EMG filtering")
    emg_amplification = models.IntegerField(blank=True,null=True,verbose_name = "amplification")
    
    def __unicode__(self):
        return 'EMG Channel: %s (Muscle: %s, Side: %s) '  % (self.name, self.sensor.muscle.label, self.sensor.side.label)  
    class Meta:
        verbose_name = "EMG channel"


class SonoChannel(Channel):
    sono_unit = models.ForeignKey(Sonounit, verbose_name="EMG units")
    crystal1 = models.ForeignKey(SonoSensor, related_name="crystals1_related")
    crystal2 = models.ForeignKey(SonoSensor, related_name="crystals2_related")

    def __unicode__(self):
        return 'Sono Channel: %s (Muscle: %s, Side: %s, Crystal1: %s, Crystal2: %s) '  % (self.name, self.crystal1.muscle.label, self.crystal1.side.label, self.crystal1.name, self.crystal2.name)  

    class Meta:
        verbose_name = "sonochannel"
               
class Session(FeedBaseModel):
    accession = models.CharField(max_length=255, blank = True, null=True)
    title = models.CharField(max_length=255, default="new Recording Session - edit this")
    bookkeeping = models.CharField("bookkeeping", max_length=255,blank = True, null=True)
    experiment = models.ForeignKey(Experiment)    
    position = models.IntegerField(help_text='the order of the recording session in the experiment')
    start = models.DateTimeField( blank = True, null=True, help_text='format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00')
    end = models.DateTimeField(blank = True, null=True, help_text='format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00')
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
    title = models.CharField(max_length=255, default='new Trial - edit this')
    bookkeeping = models.CharField("bookkeeping", max_length=255,blank = True, null=True)
    session = models.ForeignKey(Session)    
    position = models.IntegerField()
    start = models.DateTimeField( blank = True, null=True, help_text='format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00')
    end = models.DateTimeField(blank = True, null=True, help_text='format: yyyy-mm-dd hh:mm:ss example: 1990-10-10 00:00:00')
    claimed_duration = models.DecimalField("Estimated duration (seconds)",max_digits=8, decimal_places=4, blank = True, null=True)    
    subj_treatment = models.TextField("subject treatment",blank = True, null=True)
    subj_notes = models.TextField("subject notes", blank = True, null=True)

    food_type = models.CharField("food type", max_length=255,blank = True, null=True)
    food_size = models.CharField("Food size (maximum dimension millimeters)", max_length=255,blank = True, null=True)
    food_property = models.CharField("food property", max_length=255,blank = True, null=True)

    behavior_primary = models.ForeignKey(Behavior,verbose_name="primary behavior")
    behavior_secondary = models.CharField("secondary behavior", max_length=255,blank = True, null=True)
    behavior_notes = models.TextField("behavior notes", blank = True, null=True)

    waveform_picture = models.FileField("waveform picture",upload_to="pictures",  blank = True, null=True)
    data_file  = models.FileField("Data File",upload_to=get_data_upload_to ,  blank = True, null=True)

    def __unicode__(self):
        return self.title          

class Illustration(FeedBaseModel):
    picture = models.FileField("picture",upload_to='illustrations',  blank = True, null=True)
    notes = models.TextField(blank = True, null=True)
    subject  = models.ForeignKey(Subject,  blank = True, null=True)
    setup  = models.ForeignKey(Setup,  blank = True, null=True)
    experiment  = models.ForeignKey(Experiment,  blank = True, null=True)
    
class ChannelLineup(FeedBaseModel):
    session = models.ForeignKey(Session)
    position = models.IntegerField()
    channel = models.ForeignKey(Channel)

    class Meta:
        ordering = ["position"]
        verbose_name = "Channel Position"
        verbose_name_plural = "Channel Lineup"
    def __unicode__(self):
        return str(self.position) 

class EmgElectrode(FeedBaseModel):
    sensor = models.OneToOneField(Sensor, null=True,blank=True, editable=False)
    channel = models.OneToOneField(Channel, null=True, blank=True,editable=False)
    setup = models.ForeignKey(Setup)
    name = models.CharField(max_length=255)
    notes = models.TextField( blank = True, null=True)
    muscle = models.ForeignKey(Muscle)
    side = models.ForeignKey(Side, verbose_name="side of muscle" )
    axisdepth = models.ForeignKey(DepthAxis, verbose_name="Electrode insertion depth", blank = True, null=True )
    axisap = models.ForeignKey(AnteriorPosteriorAxis, verbose_name="Anterior-posterior axis", blank = True, null=True )
    axisdv = models.ForeignKey(DorsalVentralAxis, verbose_name="Dorsal-ventral axis", blank = True, null=True )
    electrode_type = models.ForeignKey(ElectrodeType, 
        verbose_name="electrode type", blank = True, null=True )
    rate = models.IntegerField(verbose_name="Sample Rate")
    emg_unit = models.ForeignKey(Emgunit, verbose_name="EMG units")
    emg_filtering = models.ForeignKey(Emgfiltering, verbose_name="EMG filtering")
    emg_amplification = models.IntegerField(blank=True,null=True,verbose_name = "amplification")

    def __unicode__(self):
        return self.name  
    
    def save(self):
        sensor = self.sensor
        if sensor ==None:
            sensor = EmgSensor()
            sensor.setup = self.setup
        sensor.created_by = self.created_by
        sensor.created_at = self.created_at
        sensor.updated_at = self.updated_at
        sensor.name = self.name
        sensor.notes = self.notes
        sensor.muscle = self.muscle
        sensor.side = self.side
        sensor.axisdepth = self.axisdepth
        sensor.axisap = self.axisap
        sensor.axisdv = self.axisdv
        sensor.electrode_type  =self.electrode_type
        sensor.save()

        channel = self.channel
        if channel == None:
            channel = EmgChannel()
            channel.setup = self.setup
            channel.sensor = sensor
        channel.created_by = self.created_by
        channel.created_at = self.created_at
        channel.updated_at = self.updated_at
        channel.name = self.name
        channel.rate = self.rate
        channel.emg_unit = self.emg_unit
        channel.emg_amplification = self.emg_amplification
        channel.emg_filtering = self.emg_filtering
        channel.notes= self.notes
        channel.save()

        self.sensor = sensor
        self.channel = channel
        super(EmgElectrode, self).save()

    def delete(self):
        super(EmgElectrode, self).delete()
        if self.channel !=None:
            self.channel.delete()
        if self.sensor !=None:
            self.sensor.delete()

        
        
    class Meta:
        verbose_name = "EMG Electrode"
        verbose_name_plural = "EMG Electrodes" 

