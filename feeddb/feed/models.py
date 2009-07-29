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
    
#cvterms
class CvTerm(FeedBaseModel):
    label = models.CharField(max_length=255)
    controlled = models.BooleanField()
    deprecated = models.BooleanField()
    def __unicode__(self):
        return self.label
    class Meta:
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

class Muscle(CvTerm):
    pass

class Side(CvTerm):
    pass

class DepthAxis(CvTerm):
    pass

class AnteriorPosteriorAxis(CvTerm):
    pass

class DorsalVentralAxis(CvTerm):
    pass

class EletrodeType(CvTerm):
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
                
