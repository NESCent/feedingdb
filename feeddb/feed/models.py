from django.db import models
from django.contrib.auth.models import User
import datetime


# base model for the whole project

class FeedBaseModel(models.Model):
    created_by = models.ForeignKey(User,editable=False, blank=True, null=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
   
    class Meta:
        abstract = True

    def save(self):
        if not self.id:
            self.created_at = datetime.date.today()
        self.updated_at = datetime.datetime.today()
        super(FeedBaseModel, self).save()
    def _view_link(self):
        return "view"
    view = property(_view_link)

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

class Behavior(CvTerm):
    pass

class Taxon(CvTerm):
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
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
        verbose_name_plural = "Depth axes"


class AnteriorPosteriorAxis(CvTerm):
    class Meta:
        verbose_name_plural = "Anterior posterior axes"


class DorsalVentralAxis(CvTerm):
    class Meta:
        verbose_name_plural = "Dorsal ventral axes"


class EletrodeType(CvTerm):
    pass

class Behavior(CvTerm):
    pass

class Restraint(CvTerm):
    pass

#object models    
class Study(FeedBaseModel):
    accession = models.CharField(max_length=255, blank = True, null=True)
    name = models.CharField(max_length=255)
    bookkeeping = models.CharField("Book keeping",max_length=255, blank = True, null=True)
    start = models.DateTimeField(blank = True, null=True)
    end = models.DateTimeField( blank = True, null=True)
    funding_agency = models.CharField(max_length=255, blank = True, null=True)
    approval_secured = models.CharField(max_length=255, blank = True, null=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Studies"

class StudyPrivate(FeedBaseModel):
    study = models.ForeignKey(Study)
    pi = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank = True, null=True)
    lab = models.CharField(max_length=255, blank = True, null=True)
    funding = models.CharField(max_length=255, blank = True, null=True)
    approval = models.CharField(max_length=255, blank = True, null=True)
    notes = models.TextField( blank = True, null=True)

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
    notes = models.TextField(blank = True, null=True)
    def __unicode__(self):
        return self.name        
        
class Experiment(FeedBaseModel):
    study = models.ForeignKey(Study)    
    subject = models.ForeignKey(Subject)    
    accession = models.CharField(max_length=255, blank = True, null=True)
    start = models.DateTimeField( blank = True, null=True)
    end = models.DateTimeField(blank = True, null=True)
    bookkeeping = models.CharField("Book Keeping", max_length=255,blank = True, null=True)
    description = models.TextField()
    subj_devstage = models.ForeignKey(DevelopmentStage,verbose_name="Subject Development Stage")
    subj_age = models.DecimalField("Subject Age",max_digits=19, decimal_places=5, blank = True, null=True)
    subj_weight = models.DecimalField("Subject Weight",max_digits=19, decimal_places=5, blank = True, null=True)
    subj_tooth = models.CharField("Subject Tooth",max_length=255, blank = True, null=True)
    subject_notes = models.TextField("Subject Notes", blank = True, null=True)
    impl_notes = models.TextField("Implantation Notes", blank = True, null=True)
    def __unicode__(self):
        return self.description    
    

class Sensor(FeedBaseModel):
    technique = models.ForeignKey(Technique)    
    experiment = models.ForeignKey(Experiment)    
    name = models.CharField(max_length=255)
    notes = models.TextField( blank = True, null=True)
    muscle = models.ForeignKey(Muscle )
    side = models.ForeignKey(Side, verbose_name="Side of muscle" )
    axisdepth = models.ForeignKey(DepthAxis, verbose_name="Depth axis", blank = True, null=True )
    axisap = models.ForeignKey(AnteriorPosteriorAxis, verbose_name="Anterior posterior axis", blank = True, null=True )
    axisdv = models.ForeignKey(DorsalVentralAxis, verbose_name="Dorsal ventral axis", blank = True, null=True )
    eletrode_type = models.ForeignKey(EletrodeType, verbose_name="Eletrode type", blank = True, null=True )
    def __unicode__(self):
        return ' '.join([self.name, "(", self.muscle.label, ", ", self.side.label, ")"])  
                
class Session(FeedBaseModel):
    experiment = models.ForeignKey(Experiment)    
    accession = models.CharField(max_length=255, blank = True, null=True)
    start = models.DateTimeField( blank = True, null=True)
    end = models.DateTimeField(blank = True, null=True)
    position = models.IntegerField()
    bookkeeping = models.CharField("Book Keeping", max_length=255,blank = True, null=True)
    subj_restraint = models.ForeignKey(Restraint,verbose_name="Subject Restraint")
    subj_anesthesia_sedation = models.CharField("Subject Anesthesia Sedation", max_length=255,  blank = True, null=True)
    subj_notes = models.TextField("Subject Notes", blank = True, null=True)

    def __unicode__(self):
        return "Session %s" % str(self.position)           

    class Meta:
        ordering = ["position"]

class Trial(FeedBaseModel):
    session = models.ForeignKey(Session)    
    accession = models.CharField(max_length=255, blank = True, null=True)
    position = models.IntegerField()
    start = models.DateTimeField( blank = True, null=True)
    end = models.DateTimeField(blank = True, null=True)
    claimed_duration = models.DecimalField("Claimed duration",max_digits=8, decimal_places=4, blank = True, null=True)    
    bookkeeping = models.CharField("Book Keeping", max_length=255,blank = True, null=True)
    subj_treatment = models.TextField("Subject Treatment",blank = True, null=True)
    subj_notes = models.TextField("Subject Notes", blank = True, null=True)
    food_type = models.CharField("Food Type", max_length=255,blank = True, null=True)
    food_size = models.CharField("Food Size", max_length=255,blank = True, null=True)
    food_property = models.CharField("Food Property", max_length=255,blank = True, null=True)
    behavior_primary = models.ForeignKey(Behavior,verbose_name="Primary Behavior")
    behavior_secondary = models.CharField("Secondary Behavior", max_length=255,blank = True, null=True)
    behavior_notes = models.TextField("Behavior Notes", blank = True, null=True)
    waveform_picture = models.FileField("Wave Form Picture",upload_to="pictures" ,  blank = True, null=True)

    def __unicode__(self):
        return "Trail %s" % str(self.position)          
'''
class Channel(FeedBaseModel):
    name = models.CharField(max_length = 255)
    def __unicode__(self):
        return name          
'''
