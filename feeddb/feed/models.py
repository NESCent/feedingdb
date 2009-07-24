from django.db import models
#from django.contrib.auth.models import User
#import datetime

# base model for the whole project
"""
class FeedBaseModel(models.Model):
    created_by = models.ForeignKey(User,editable=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    def save(self):
        if not self.id:
            self.created_at = datetime.date.today()
        self.updated_at = datetime.datetime.today()
        super(FeedBaseModel, self).save()
    def save(self,request=None):
        if not self.id:
            self.created_at = datetime.date.today()
        self.updated_at = datetime.datetime.today()
        self.created_by = request.user
        super(FeedBaseModel, self).save()
"""    
#cvterms
class CvTerm(models.Model):
    label = models.CharField(max_length=255)
    controlled = models.BooleanField()
    deprecated = models.BooleanField()
    def __unicode__(self):
        return self.label

class CvDevStage(CvTerm):
    pass

class CvTechnique(CvTerm):
    pass

class CvBehavior(CvTerm):
    pass

class CvTaxon(CvTerm):
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.species + " " + self.genus

#object models    
class Study(models.Model):
    accession = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    bookkeeping = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    funding_agency = models.CharField(max_length=255)
    approval_secured = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class StudyPrivate(models.Model):
    study = models.ForeignKey(Study)
    pi = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    lab = models.CharField(max_length=255)
    funding = models.CharField(max_length=255)
    approval = models.CharField(max_length=255)
    notes = models.TextField()

class Subject(models.Model):
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    
    study = models.ForeignKey(Study)
    taxon = models.ForeignKey(CvTaxon)
    name = models.CharField(max_length=255)    
    breed = models.CharField(max_length=255)   
    sex = models.CharField(max_length=2, choices = GENDER_CHOICES) 
    source = models.CharField(max_length=255) 
    notes = models.TextField()
    def __unicode__(self):
        return self.name        
        
class Experiment(models.Model):
    list_display = ('start', 'end','bookkeeping', 'subject')
    list_display_links = ('bookkeeping')
    study = models.ForeignKey(Study)    
    subject = models.ForeignKey(Subject)    
    accession = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    bookkeeping = models.CharField(max_length=255)
    description = models.TextField()
    subj_devstage = models.ForeignKey(CvDevStage,verbose_name="Subject development stage")
    subj_age = models.DecimalField("subject age",max_digits=19, decimal_places=5)
    subj_tooth = models.CharField("subject tooth",max_length=255)
    subject_notes = models.CharField("subject notes", max_length=255)
    impl_notes = models.CharField("impl. notes", max_length=255)
    def __unicode__(self):
        return self.accession    
    
            