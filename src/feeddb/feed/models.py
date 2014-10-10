from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch

from django.conf import settings
import datetime
from django.db.models.expressions import F


DATETIME_HELP_TEXT = ''
# Only used for Trial here; the other containers are are affected through forms.py -- go figure (VG)
BOOKKEEPING_HELP_TEXT = 'Enter any text required for lab bookkeeping concerning the Study here'

class FeedUserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    institutional_affiliation = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

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

    def get_absolute_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        try:
            return reverse('admin:%s_%s_view' % (content_type.app_label, content_type.model), args=(self.id,))
        except NoReverseMatch:
            return reverse('admin:%s_%s_change' % (content_type.app_label, content_type.model), args=(self.id,))

    def save(self):
        now = datetime.datetime.today()
        if not self.id:
            self.created_at = now
        self.updated_at = now
        super(FeedBaseModel, self).save()

class OwlTerm(models.Model):
    label = models.CharField(max_length=1000)
    # TODO: see gl-4
    #rdf_type = models.CharField(max_length=255)
    obo_definition = models.TextField()
    rdfs_comment = models.TextField()
    uri = models.CharField(max_length=1500)

    # Whether this term had an rdfs:type relation to the rdfs:Class object in
    # the original OWL file.
    rdfs_is_class = models.BooleanField(default=False)

    # The list of parent terms and parents of parent terms, and so on.
    # Determined by the rdfs:subClassOf property.
    rdfs_subClassOf_ancestors = models.ManyToManyField('self',
        symmetrical=False, related_name='has_subClass_descendants')
    # The list of child terms and grandchild terms, and so on. Determined by
    # the rdfs:subClassOf property.
    #rdfs_subClassOf_descendants = models.ManyToManyField('self', symmetrical=false)

    bfo_part_of_some = models.ManyToManyField('self',
        symmetrical=False, related_name='has_parts')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.label

    def cloneable(self):
        return False

    @staticmethod
    def default_qs_filter_args():
        """
        Return the default filter dict for a queryset against this model.

        In subclasses, this should be overridden to ensure that we only use
        terms which are supposed to be used.
        """
        return dict(rdfs_is_class=True)

    @classmethod
    def default_qs(cls):
        return cls.objects.filter(**(cls.default_qs_filter_args())).order_by('label')

    def part_of_classes(self):
        return self.bfo_part_of_some.filter(**(self.default_qs_filter_args()))

    def part_of_classes_inclusive(self):
        return [self] + list(self.part_of_classes())

    def ancestor_classes(self):
        return self.rdfs_subClassOf_ancestors.filter(**(self.default_qs_filter_args()))

    def ancestor_classes_inclusive(self):
        return [self] + list(self.ancestor_classes())

class MuscleOwl(OwlTerm):

    @staticmethod
    def default_muscle():
        return MuscleOwl.objects.get(label='muscle organ')

    @staticmethod
    def default_qs_filter_args():
        return dict(
            # This is the "muscle organ" class, which is specified by Hilmar as
            # the ultimate ancestor class for muscles
            #
            # URI: http://purl.obolibrary.org/obo/UBERON_0001630
            rdfs_subClassOf_ancestors__label='muscle organ'
        )

class BehaviorOwl(OwlTerm):

    @staticmethod
    def default_qs_filter_args():
        return dict(
            # This is the "behavior" class, which may or may not be an appropriate filter
            rdfs_subClassOf_ancestors__uri=u'http://purl.obolibrary.org/obo/OPBO_0000011'

            # Other options include:
            #
            # >>> print "\n".join(["%s - %s" % (b.uri, b.label) for b in BehaviorOwl.objects.filter(label__contains='behavior') ])
            # http://purl.obolibrary.org/obo/GO_0051705 - multi-organism behavior
            # http://purl.obolibrary.org/obo/OPBO_0000012 - oral/pharyngeal behavior
            # http://purl.obolibrary.org/obo/OPBO_0000011 - behavior
            # http://purl.obolibrary.org/obo/OPBO_0000017 - feeding behavior
            # http://purl.obolibrary.org/obo/OPBO_0000018 - ingestion behavior
            # http://purl.obolibrary.org/obo/GO_0007610 - behavior
            # http://purl.obolibrary.org/obo/GO_0007631 - feeding behavior
            #
        )

#cvterms
class CvTerm(FeedBaseModel):
    label = models.CharField(max_length=255)
    is_cloneable = False

    def __unicode__(self):
        return self.label
    class Meta:
        ordering = ["label"]
        abstract = True

class AnimalApprovalType(FeedBaseModel):
    description = models.TextField()
    is_cloneable = False

    def __unicode__(self):
        return self.description

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

TECHNIQUE_CHOICES_NAMED = (
               (u'emgsetup', u'EMG'),
               (u'sonosetup', u'Sono'),
               (u'strainsetup', u'Strain'),
               (u'forcesetup', u'Bite force'),
               (u'pressuresetup', u'Pressure'),
               (u'kinematicssetup', u'Kinematics'),
               (u'eventsetup', u'Time/Event'),
               (u'othersetup', u'Other'),
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

    @classmethod
    def num2label(cls, num):
        return cls.__choices_dict.get(num, "Unknown Technique")

    @classmethod
    def name2num(cls, name):
        i = 1
        for n, l in TECHNIQUE_CHOICES_NAMED:
            if n == name:
               return i
            ++i
        return None

    @classmethod
    def get_setup_model(cls, technique):
        if technique == cls.ENUM.emg:
            return EmgSetup
        elif technique == cls.ENUM.sono:
            return SonoSetup
        elif technique == cls.ENUM.strain:
            return StrainSetup
        elif technique == cls.ENUM.force:
            return ForceSetup
        elif technique == cls.ENUM.pressure:
            return PressureSetup
        elif technique == cls.ENUM.kinematics:
            return KinematicsSetup
        elif technique == cls.ENUM.event:
            return EventSetup

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

    # equivalent OWL term for migration
    ontology_term = models.ForeignKey(MuscleOwl, related_name="+", null=True)
    class Meta:
        verbose_name = 'Anatomical Location'
        verbose_name_plural = 'Anatomical Locations'

class Side(CvTerm):
    pass

class DepthAxis(CvTerm):
    class Meta:
        verbose_name = "Depth Point"
        verbose_name_plural = "Depth Axis"


class AnteriorPosteriorAxis(CvTerm):
    class Meta:
        verbose_name = "Anterior-posterior Point"
        verbose_name_plural = "Anterior-posterior Axis"


class DorsalVentralAxis(CvTerm):
    class Meta:
        verbose_name = "Dorsal-ventral Point"
        verbose_name_plural = "Dorsal-ventral Axis"

class ProximalDistalAxis(CvTerm):
    class Meta:
        verbose_name = "Proximal-distal Point"
        verbose_name_plural = "Proximal-distal Axis"

class MedialLateralAxis(CvTerm):
    class Meta:
        verbose_name = "Medial-lateral Point"
        verbose_name_plural = "Medial-lateral Axis"


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
    class Meta:
        verbose_name = "EMG Filtering"
        verbose_name_plural = "EMG Filterings"

#object models
class Study(FeedBaseModel):
    title = models.CharField(max_length=255,
                             help_text = "Enter a short title for the Study here")
    bookkeeping = models.CharField("Bookkeeping",max_length=255, blank = True, null=True, help_text = BOOKKEEPING_HELP_TEXT)
    start = models.DateField("Start Date", null=False)
    end = models.DateField("End Date", blank = True, null=True)
    funding_agency = models.CharField(max_length=255, blank = True, null=True,
                             help_text = "The agency that funded the research")

    approval_type = models.ForeignKey(AnimalApprovalType, verbose_name="Approval Secured", blank=False, null=True,
                             help_text =
                                '''
                                Affirmation that an institutional approval for
                                Animal Care and Use or for Human Subjects was
                                secured. Please read each statement very
                                carefully. Data upload can not continue without
                                checking the appropriate affirmation.
                                ''')

    description = models.TextField("Study Description",
                             help_text = "A brief summary of the Study goals and data")
    resources = models.TextField("External Resources", blank = True, null=True,
                             help_text = "Published or other types of information relevant to interpreting the physiologic data can be cited here")

    # Previously private fields
    approval = models.CharField("Animal Use Approval (if applicable)", max_length=255, blank = True, null=True,
                                help_text = "A reference to approval documentation for Animal Care and Use or for Human Subjects, if it was secured.")

    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Studies"

class StudyPrivate(FeedBaseModel):
    study = models.OneToOneField(Study)

    pi = models.CharField("Lab PI", max_length=255, null=True,
                             help_text = "The name of the PI of the lab where the data were collected and/or the grant that funded the research")
    notes = models.TextField("Private Notes", blank=True, null=True)

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
    title = models.CharField(max_length=255)
    bookkeeping = models.CharField("Bookkeeping", max_length=255,blank = True, null=True, help_text = BOOKKEEPING_HELP_TEXT)
    study = models.ForeignKey(Study)
    subject = models.ForeignKey(Subject)
    start = models.DateField("Start Date", null=True, help_text=DATETIME_HELP_TEXT)
    end = models.DateField("End Date", blank = True, null=True, help_text=DATETIME_HELP_TEXT)
    description = models.TextField(blank = True, null=True)
    subj_devstage = models.ForeignKey(DevelopmentStage,verbose_name="Subject Development Stage")
    subj_age = models.DecimalField("Subject Age",max_digits=19, decimal_places=5, blank = True, null=True,
                                   help_text = "As a decimal; use the following field to specify age units.")
    subj_ageunit = models.ForeignKey(AgeUnit, verbose_name='Age Units', blank = True, null = True)
    subj_weight = models.DecimalField("subject Weight (kg)",max_digits=19, decimal_places=5, blank = True, null=True)
    subj_tooth = models.CharField("Subject Teeth",max_length=255, blank = True, null=True,
                                  help_text = "Stage of teeth development")
    subject_notes = models.TextField("Subject Notes", blank = True, null=True)
    impl_notes = models.TextField("Implantation Notes", blank = True, null=True)
    def __unicode__(self):
        return self.title

    def has_setup_type(self, name, freshen=False):
        """
        Determine if the experiment has a setup of the specified type.
        """
        for setup in self.get_setups(freshen):
            if hasattr(setup, name):
                return True
        return False

    def get_setups(self, freshen=False):
        """
        Uses an instance variable to cache results of the query; pass
        "freshen=True" to force a new query.
        """
        if not hasattr(self, '_setups') or freshen:
            self._setups = list(self.setup_set.order_by('pk'))

        return self._setups

    def get_setups_with_type(self, freshen=False):
        if not hasattr(self, '_setup_types') or freshen:
            self._setup_types = self._get_setup_types(self.get_setups(freshen=freshen))

        return zip(self._setup_types, self._setups)

    @staticmethod
    def _get_setup_types(setups):
        types = []
        for setup in setups:
            for setup_name, label in TECHNIQUE_CHOICES_NAMED:
                if hasattr(setup, setup_name):
                    types.append(setup_name)
                    break
            else:
                # if no known type was found, save "unknown" as the type
                types.append('unknown')

        return types

class Setup(FeedBaseModel):
    is_cloneable=False
    study = models.ForeignKey(Study)
    experiment = models.ForeignKey(Experiment)
    technique = models.IntegerField(choices=Techniques.CHOICES)
    notes = models.TextField("Notes about all sensors and channels in this setup", blank = True, null=True)
    sampling_rate = models.IntegerField("Sampling Rate (Hz)", blank=True, null=True)
    class Meta:
        verbose_name = "Setup"

    def save(self):
        self.study = self.experiment.study
        return super(Setup, self).save()

class EmgSetup(Setup):
    preamplifier = models.CharField(max_length=255, blank = True, null=True)
    class Meta:
        verbose_name = "EMG Setup"

class SonoSetup(Setup):
    sonomicrometer = models.CharField(max_length=255, blank = True, null=True)
    class Meta:
        verbose_name = "Sono Setup"

class StrainSetup(Setup):
    class Meta:
        verbose_name = "Strain Setup"

class ForceSetup(Setup):
    class Meta:
        verbose_name = "Bite Force Setup"

class PressureSetup(Setup):
    class Meta:
        verbose_name = "Pressure Setup"

class KinematicsSetup(Setup):
    class Meta:
        verbose_name = "Kinematics Setup"

    def save(self):
        if self.notes in (None, '') and self.id == None:
            self.notes = 'camera\nmarkers\nmovie film or digital\nlight or x-ray\nanatomical view (lateral/d-v/frontal)\n2D or 3D'
        super(KinematicsSetup, self).save()

class EventSetup(Setup):
    class Meta:
        verbose_name = "Time/Event Setup"


class Sensor(FeedBaseModel):
    study = models.ForeignKey(Study, null=True)
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

    def save(self):
        self.study = self.setup.study
        return super(Sensor, self).save()

class EmgSensor(Sensor):
    location_controlled = models.ForeignKey(AnatomicalLocation, verbose_name = "Muscle", null=False,
                                            limit_choices_to = {'category__exact' : AnatomicalCategories.muscle})
    muscle = models.ForeignKey(MuscleOwl, verbose_name = "Muscle (OWL)", null=True, limit_choices_to=MuscleOwl.default_qs_filter_args())

    axisdepth = models.ForeignKey(DepthAxis, verbose_name="Electrode Depth", blank = True, null=True )
    electrode_type = models.ForeignKey(ElectrodeType,
        verbose_name="Electrode Type", blank = True, null=True )

    def __unicode__(self):
        return 'EMG Sensor: %s (Muscle: %s, Side: %s) '  % (self.name, self.location_controlled.label, self.loc_side.label)

    class Meta:
        verbose_name = "EMG Electrode"
        ordering = ["id"]

class SonoSensor(Sensor):
    location_controlled = models.ForeignKey(AnatomicalLocation, verbose_name = "Muscle", null=False,
                                            limit_choices_to = {'category__exact' : AnatomicalCategories.muscle})
    muscle = models.ForeignKey(MuscleOwl, verbose_name = "Muscle (OWL)", null=True, limit_choices_to=MuscleOwl.default_qs_filter_args())

    axisdepth = models.ForeignKey(DepthAxis, verbose_name="Crystal Depth", blank = True, null=True )
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Sono Crystal"

class StrainSensor(Sensor):
    class Meta:
        verbose_name = "Strain Sensor"

class ForceSensor(Sensor):
    class Meta:
        verbose_name = "Bite Force Sensor"

class PressureSensor(Sensor):
    class Meta:
        verbose_name = "Pressure Sensor"

class KinematicsSensor(Sensor):
    class Meta:
        verbose_name = "Kinematics Marker"


class Channel(FeedBaseModel):
    study = models.ForeignKey(Study, null=True)
    setup = models.ForeignKey(Setup)
    name = models.CharField(max_length = 255)
    rate = models.IntegerField("Recording Rate (Hz)")
    notes = models.TextField("Notes",  blank = True, null=True)

    def __unicode__(self):
        return self.name

    def save(self):
        self.study = self.setup.study
        return super(Sensor, self).save()

class EmgChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.emg},
                             verbose_name="EMG Units [from models.py]")
    sensor = models.ForeignKey(EmgSensor)
    emg_filtering = models.ForeignKey(Emgfiltering, verbose_name="EMG Filtering")
    emg_amplification = models.IntegerField(blank=True,null=True,verbose_name = "Amplification")

    def __unicode__(self):
        return 'EMG Channel: %s (Muscle: %s, Side: %s) '  % (self.name, self.sensor.location_controlled.label, self.sensor.loc_side.label)
    class Meta:
        verbose_name = "EMG Channel"


class SonoChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.sono},
                             verbose_name="Sono Units")
    crystal1 = models.ForeignKey(SonoSensor, related_name="crystals1_related")
    crystal2 = models.ForeignKey(SonoSensor, related_name="crystals2_related")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Sono Channel"

class StrainChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.strain},
                             verbose_name="Strain Units", null=True)
    sensor = models.ForeignKey(StrainSensor)
    class Meta:
        verbose_name = "Strain Channel"

class ForceChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.force},
                             verbose_name="Bite Force Units", null=True)
    sensor = models.ForeignKey(ForceSensor)
    class Meta:
        verbose_name = "Bite Force Channel"

class PressureChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.pressure},
                             verbose_name="Pressure Units", null=True)
    sensor = models.ForeignKey(PressureSensor)
    class Meta:
        verbose_name = "Pressure Channel"

class KinematicsChannel(Channel):
    unit = models.ForeignKey(Unit, limit_choices_to = {'technique__exact' : Techniques.ENUM.kinematics},
                             verbose_name="Kinematics Units", null=True)
    sensor = models.ForeignKey(KinematicsSensor, verbose_name="Marker")
    class Meta:
        verbose_name = "Kinematics Channel"

class EventChannel(Channel):
    unit = models.CharField(max_length=255, blank = True, null = True)
    #Note: An EventChannel is not associated with any Sensor
    class Meta:
        verbose_name = "Time/Event Channel"


class Session(FeedBaseModel):
    title = models.CharField(max_length=255)
    bookkeeping = models.CharField("Bookkeeping", max_length=255,blank = True, null=True, help_text = BOOKKEEPING_HELP_TEXT)
    study = models.ForeignKey(Study)
    experiment = models.ForeignKey(Experiment)
    position = models.IntegerField(help_text='The numeric position of this recording session among the other sessions within the current experiment.')
    start = models.DateField(null=True, help_text=DATETIME_HELP_TEXT)
    end = models.DateField(blank = True, null=True, help_text=DATETIME_HELP_TEXT)
    subj_notes = models.TextField("Subject Notes", blank = True, null=True)
    subj_restraint = models.ForeignKey(Restraint,verbose_name="Subject Restraint")
    subj_anesthesia_sedation = models.CharField("Subject Anesthesia / Sedation", max_length=255,  blank = True, null=True)

    channels  = models.ManyToManyField(Channel, through='ChannelLineup')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["position"]

    def save(self):
        self.study = self.experiment.study
        return super(Session, self).save()


# function to decide the upload_to for trial data file
# upload_to = [media_root]/data/study_[study id]/experiment_[experiment id]/session_[session id]
def get_data_upload_to(instance, filename):
    session=instance.session
    experiment = session.experiment
    study = experiment.study
    return 'data/study_%d/experiment_%d/session_%d/%s' % (study.id, experiment.id,session.id, filename)

class Trial(FeedBaseModel):
    title = models.CharField(max_length=255)
    bookkeeping = models.CharField("Bookkeeping", max_length=255,blank = True, null=True, help_text = BOOKKEEPING_HELP_TEXT)
    session = models.ForeignKey(Session)
    experiment = models.ForeignKey(Experiment)
    study = models.ForeignKey(Study)
    position = models.IntegerField(help_text='The numeric position of this trial among the other trials within the current recording session.')
    start = models.DateField(null=True, help_text = DATETIME_HELP_TEXT)
    end = models.DateField(blank = True, null=True, help_text = DATETIME_HELP_TEXT)
    subj_treatment = models.TextField("Subject Treatment",blank = True, null=True)
    subj_notes = models.TextField("Subject Notes", blank = True, null=True)

    food_type = models.CharField("Food Type", max_length=255,blank = True, null=True)
    food_size = models.CharField("Food Size (maximum dimension millimeters)", max_length=255,blank = True, null=True)
    food_property = models.CharField("Food Property", max_length=255,blank = True, null=True)

    is_calibration = models.BooleanField("This is a Calibration", help_text="You must either check this box or select a Feeding Behavior for this trial.", default=False)

    # deprecated in FEED2
    behavior_primary = models.ForeignKey(Behavior, verbose_name="Primary Behavior", null=True, blank=True)

    behaviorowl_primary = models.ForeignKey(BehaviorOwl,
        verbose_name="Feeding Behavior",
        null=True,
        blank=True,
        related_name="primary_in_trials",
        limit_choices_to=BehaviorOwl.default_qs_filter_args(),
        help_text="You must choose a Feeding Behavior unless you have checked that this is a Calibration Trial.")

    # deprecated in FEED2
    behavior_secondary = models.CharField("Secondary Behavior", max_length=255,blank = True, null=True)

    behavior_notes = models.TextField("Behavior Notes", blank = True, null=True)

    data_file  = models.FileField(verbose_name="Data File",upload_to=get_data_upload_to ,  blank = True, null=True,
                                  help_text="A tab-delimited file with columns corresponding to the channel lineup specified in the Recording Session.")
    waveform_picture = models.FileField(verbose_name="Illustration", upload_to="pictures",  blank = True, null=True,
                                        help_text="A picture (jpeg, pdf, etc.) as a graphical overview of data in the data file.")

    def __unicode__(self):
        return self.title
    def taxon_name(self):
        return self.session.experiment.subject.taxon.label
    taxon_name.short_description = 'Species'
    taxon_name.admin_order_field = 'session__experiment__subject__taxon__label'

    def save(self):
        self.experiment = self.session.experiment
        self.study = self.session.study
        return super(Trial, self).save()

class Illustration(FeedBaseModel):
    picture = models.FileField(verbose_name="Picture",upload_to='illustrations',  blank = True, null=True)
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

