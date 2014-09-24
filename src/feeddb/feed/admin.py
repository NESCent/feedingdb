from feeddb.feed.models import *
from django.contrib import admin
from django import forms
from django.forms import models
from feeddb.feed.extension.modeladmin import *
from feeddb.feed.extension.forms import *
from feeddb.feed.extension.formsets import *

from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

class ExperimentViewInline(FeedTabularInline):
    model = Experiment
    extra = 0
    tabbed = True
    fields = ['title', 'subject','subj_devstage','start','end']
    tab_name = "Experiments"

class IllustrationInline(FeedTabularInline):
    model = Illustration
    extra = 1
    fields = ('picture','notes')

class IllustrationViewInline(FeedTabularInline):
    model = Illustration
    extra = 0
    fields = ('picture', 'notes')

class SessionViewInline(FeedTabularInline):
    model = Session
    extra = 0
    fields = ('title', 'start', 'position', 'subj_restraint', 'subj_anesthesia_sedation')
    tabbed = True
    tab_name = 'Sessions'

class TrialViewInline(FeedTabularInline):
    model = Trial
    extra = 0
    fields = ('position', 'title', 'food_type', 'behavior_primary')
    tabbed = True
    tab_name="Trials"


class SubjectViewInline(FeedTabularInline):
    model = Subject
    extra = 0
    tabbed = True
    tab_name="Subjects"

class StudyAdmin(FeedModelAdmin):
    view_inlines = [SubjectViewInline, ExperimentViewInline, SessionViewInline, TrialViewInline]
    search_fields = ('title', 'description')
    list_display = ('title','start','end', 'funding_agency',)
    # exclude old "approval" field
    exclude = ('approval',)
    form = StudyChangeForm
    tabbed = False

class ExperimentAdmin(ExperimentModelAdmin):
    inlines = [IllustrationInline]
    view_inlines = [IllustrationViewInline]
    search_fields = ('title','study__title','subject__taxon__genus','subject__taxon__species','subject__taxon__common_name','subject__name','description','subject_notes','impl_notes')
    list_display = ('title','study', 'subject','subj_devstage')
    form = ExperimentChangeForm
    #list_filter = ('study', 'subject')



class SubjectAdmin(FeedModelAdmin):
    inlines = [IllustrationInline]
    view_inlines = [IllustrationViewInline]
    search_fields = ('name','study__title', 'breed','taxon__species', 'taxon__genus','taxon__common_name','source','sex','notes')
    list_display = ('name', 'study', 'taxon', 'breed','sex', 'source')
    #list_filter = ('study', 'taxon','sex')
    ordering = ('name',)
    form = DisableForeignKeyForm

class TrialAdmin(FeedModelAdmin):
    form = TrialForm
    search_fields = ('title','bookkeeping','subj_notes','subj_treatment','food_type','food_property','behavior_primary__label','behavior_secondary','behavior_notes')
    list_display = ('title', 'session', 'taxon_name','food_type', 'behavior_primary','waveform_picture')
    form = TrialChangeForm
    # hide old non-OWL behavior fields
    exclude = ('behavior_primary','behavior_secondary',)
    ordering = ('position',)
    form = DisableForeignKeyForm

class IllustrationAdmin(FeedModelAdmin):
    search_fields = ('notes', 'experiment','setup', 'subject')
    list_display = ('picture', 'notes')
    #list_filter = ('experiment', 'subject')
    ordering = ('picture',)

class EmgSensorViewInline(FeedTabularInline):
    model = EmgSensor
    exclude = ['location_freetext']
    extra = 0
    form = EmgSensorChannelForm

class EmgSensorInline(FeedTabularInline):
    model = EmgSensor
    exclude = ['location_controlled', 'location_freetext']
    extra = 5
    form = EmgSensorChannelForm
    formset = OrderedFormset

class SonoSensorInline(SetupTabularInline):
    model = SonoSensor
    extra = 4
    exclude = ['location_controlled', 'location_freetext']
    form = SonoSensorForm

class SonoSensorViewInline(FeedTabularInline):
    model = SonoSensor
    extra = 0
    exclude = ['location_controlled', 'location_freetext']
    form = SonoSensorForm

class StrainSensorInline(SetupTabularInline):
    model = StrainSensor
    extra = 3
    form = StrainSensorForm

class StrainSensorViewInline(FeedTabularInline):
    model = StrainSensor
    extra = 0
    form = StrainSensorForm

class ForceSensorInline(SetupTabularInline):
    model = ForceSensor
    extra = 3
    form = ForceSensorForm

class ForceSensorViewInline(FeedTabularInline):
    model = ForceSensor
    extra = 0
    form = ForceSensorForm

class PressureSensorInline(SetupTabularInline):
    model = PressureSensor
    extra = 3
    form = PressureSensorForm

class PressureSensorViewInline(FeedTabularInline):
    model = PressureSensor
    extra = 0
    form = PressureSensorForm

class KinematicsSensorInline(SetupTabularInline):
    model = KinematicsSensor
    extra = 3
    form = KinematicsSensorForm

class KinematicsSensorViewInline(FeedTabularInline):
    model = KinematicsSensor
    extra = 0
    form = KinematicsSensorForm

class ChannelInline(FeedTabularInline):
    model = Channel
    exclude = ['notes']
    extra = 0



class SonoChannelInline(FeedTabularInline):
    model = SonoChannel
    extra =5
    form = SonoChannelForm

class SonoChannelViewInline(FeedTabularInline):
    model = SonoChannel
    extra = 0

class StrainChannelInline(FeedTabularInline):
    model = StrainChannel
    extra =9
    form = StrainChannelForm

class StrainChannelViewInline(FeedTabularInline):
    model = StrainChannel
    extra = 0

class ForceChannelInline(FeedTabularInline):
    model = ForceChannel
    extra =9
    form = ForceChannelForm

class ForceChannelViewInline(FeedTabularInline):
    model = ForceChannel
    extra = 0

class PressureChannelInline(FeedTabularInline):
    model = PressureChannel
    extra =9
    form = PressureChannelForm

class PressureChannelViewInline(FeedTabularInline):
    model = PressureChannel
    extra = 0

class KinematicsChannelInline(FeedTabularInline):
    model = KinematicsChannel
    extra =9
    form = KinematicsChannelForm

class KinematicsChannelViewInline(FeedTabularInline):
    model = KinematicsChannel
    extra = 0

class EventChannelInline(FeedTabularInline):
    model = EventChannel
    extra =9
    form = EventChannelForm

class EventChannelViewInline(FeedTabularInline):
    model = EventChannel
    extra = 0

class EmgSetupAdmin(EmgSetupModelAdmin):
    inlines = [ IllustrationInline, EmgSensorInline]
    view_inlines = [IllustrationViewInline, EmgSensorViewInline]
    list_display = ('technique', 'preamplifier','experiment')
    list_filter = ('technique', 'experiment')
    ordering = ('preamplifier',)
    form = SetupForm

class SonoSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,SonoSensorInline,SonoChannelInline]
    view_inlines = [IllustrationViewInline, SonoSensorViewInline, SonoChannelViewInline]
    list_display = ('technique', 'sonomicrometer','experiment')
    list_filter = ('technique', 'experiment')
    ordering = ('sonomicrometer',)
    form = SetupForm

class StrainSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,StrainSensorInline,StrainChannelInline]
    view_inlines = [IllustrationViewInline, StrainSensorViewInline, StrainChannelViewInline]
    list_display = ('technique', 'experiment')
    list_filter = ('technique', 'experiment')
    form = SetupForm

class ForceSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,ForceSensorInline,ForceChannelInline]
    view_inlines = [IllustrationViewInline, ForceSensorViewInline, ForceChannelViewInline]
    list_display = ('technique', 'experiment')
    list_filter = ('technique', 'experiment')
    form = SetupForm

class PressureSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,PressureSensorInline,PressureChannelInline]
    view_inlines = [IllustrationViewInline, PressureSensorViewInline, PressureChannelViewInline]
    list_display = ('technique', 'experiment')
    list_filter = ('technique', 'experiment')

class KinematicsSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,KinematicsSensorInline,KinematicsChannelInline]
    view_inlines = [IllustrationViewInline, KinematicsSensorViewInline, KinematicsChannelViewInline]
    list_display = ('technique', 'experiment')
    list_filter = ('technique', 'experiment')
    form = SetupForm

class EventSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,EventChannelInline]
    view_inlines = [IllustrationViewInline, EventChannelViewInline]
    list_display = ('technique', 'experiment')
    list_filter = ('technique', 'experiment')
    form = SetupForm

class EmgChannelAdmin(DefaultModelAdmin):
    list_display = ('name', 'rate', 'sensor', 'unit', 'emg_filtering')
    ordering = ('sensor',)

class SonoChannelAdmin(DefaultModelAdmin):
    list_display = ('name', 'rate', 'crystal1','crystal2','unit')
    ordering = ('crystal1',)


class ChannelLineupInline(FeedTabularInline):
    model = ChannelLineup
    extra = 8
    tabbed = True
    tab_name="Channel Lineup"
    formset = PositionBaseInlineFormSet
    form = ChannelLineupForm

class ChannelLineupViewInline(FeedTabularInline):
    model = ChannelLineup
    extra = 0
    tab_name="Channel Lineup"
    form = ChannelLineupForm

class SessionAdmin(SessionModelAdmin):
    inlines = [ChannelLineupInline]
    view_inlines = [ChannelLineupViewInline, TrialViewInline ]
    list_display = ('title', 'experiment','position', 'start', 'subj_restraint','subj_anesthesia_sedation')
    search_fields = ('title','bookkeeping','experiment__title','subj_notes','subj_restraint__label','subj_anesthesia_sedation')
    ordering = ('position',)
    form = SessionChangeForm
    tabbed = True
    tab_name = "Session"

class EmgSensorAdmin(EmgSensorModelAdmin):
    form = EmgSensorChannelForm

class SonoSensorAdmin(DefaultModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('setup','name', 'location_controlled', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes')
        }),
    )
    ordering = ('name', 'location_controlled',)

class CommonSensorAdmin(DefaultModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('setup','name', 'location_freetext', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes')
        }),
    )
    ordering = ('name', 'location_freetext',)


class ChannelLineupAdmin(FeedModelAdmin):
    list_display = ('position', 'session','channel')
    list_filter = ('session',)
    ordering = ('session','position',)
    form = ChannelLineupForm

class TermAdmin(TermModelAdmin):
    list_display = ('label',)
    ordering = ('label',)

class UnitAdmin(TermModelAdmin):
    list_display = ('technique', 'label')
    list_filter = ('technique', )

class TaxonAdmin(TermModelAdmin):
    list_display = ('genus','species','common_name')
    ordering = ('genus','species')
    exclude = ['label']

class AnatomicalLocationAdmin(TermModelAdmin):
    list_display = ('category', 'label')
    list_filter = ('category',)
    ordering = ('category', 'label')

class FeedUserAdmin(UserAdmin):
    # disable "fancy" two-select widget for multiple-select fields
    filter_horizontal = ()

class FeedGroupAdmin(GroupAdmin):
    # disable "fancy" two-select widget for multiple-select fields
    filter_horizontal = ()

admin.site.unregister(User)
admin.site.register(User, FeedUserAdmin)

admin.site.unregister(Group)
admin.site.register(Group, FeedGroupAdmin)

admin.site.register(Taxon, TaxonAdmin)
admin.site.register(AnatomicalLocation, AnatomicalLocationAdmin)
admin.site.register(Side,TermAdmin)
admin.site.register(AnimalApprovalType)
admin.site.register(DepthAxis,TermAdmin)
admin.site.register(AnteriorPosteriorAxis,TermAdmin)
admin.site.register(DorsalVentralAxis,TermAdmin)
admin.site.register(ProximalDistalAxis,TermAdmin)
admin.site.register(MedialLateralAxis,TermAdmin)
admin.site.register(ElectrodeType,TermAdmin)
admin.site.register(DevelopmentStage,TermAdmin)
admin.site.register(AgeUnit,TermAdmin)
admin.site.register(Behavior,TermAdmin)
admin.site.register(Restraint,TermAdmin)
admin.site.register(Unit,UnitAdmin)
admin.site.register(Emgfiltering,TermAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Sensor,DefaultModelAdmin)
admin.site.register(Study,StudyAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Trial,TrialAdmin)
admin.site.register(EmgSetup,EmgSetupAdmin)
admin.site.register(SonoSetup,SonoSetupAdmin)
admin.site.register(StrainSetup,StrainSetupAdmin)
admin.site.register(ForceSetup,ForceSetupAdmin)
admin.site.register(PressureSetup,PressureSetupAdmin)
admin.site.register(KinematicsSetup,KinematicsSetupAdmin)
admin.site.register(EventSetup,EventSetupAdmin)
admin.site.register(EmgSensor, EmgSensorAdmin)
admin.site.register(SonoSensor, SonoSensorAdmin)
admin.site.register(ForceSensor, CommonSensorAdmin)
admin.site.register(StrainSensor, CommonSensorAdmin)
admin.site.register(KinematicsSensor, CommonSensorAdmin)
admin.site.register(PressureSensor, CommonSensorAdmin)
admin.site.register(ChannelLineup, ChannelLineupAdmin)
admin.site.register(Illustration,IllustrationAdmin)
#admin.site.register(EmgChannel,EmgChannelAdmin)
admin.site.register(SonoChannel,SonoChannelAdmin)
admin.site.register(Channel, DefaultModelAdmin)
admin.site.register(StrainChannel,DefaultModelAdmin)
admin.site.register(ForceChannel, DefaultModelAdmin)
admin.site.register(KinematicsChannel, DefaultModelAdmin)
admin.site.register(PressureChannel, DefaultModelAdmin)
admin.site.register(EventChannel, DefaultModelAdmin)
