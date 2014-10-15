from feeddb.feed.models import *
from django.contrib import admin
from django import forms
from django.forms import models
from feeddb.feed.extension.modeladmin import *
from feeddb.feed.extension.forms import *
from feeddb.feed.extension.formsets import *

from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

class StudyPrivateInline(admin.StackedInline):
    model = StudyPrivate
    extra = 1
    max_num = 1
    template = 'admin/edit_inline/studyprivate_stacked.html'

class ExperimentViewInline(FeedTabularInline):
    model = Experiment
    extra = 0
    tabbed = True
    fields = ['title', 'subject','subj_devstage','start','end']
    tab_name = "Experiments"
    template = 'admin/tabular_view.html'

class IllustrationInline(FeedTabularInline):
    model = Illustration
    extra = 1
    fields = ('picture','notes')

class IllustrationViewInline(FeedTabularInline):
    model = Illustration
    extra = 0
    fields = ('picture', 'notes')
    template = 'admin/tabular_view.html'

class SessionViewInline(FeedTabularInline):
    model = Session
    extra = 0
    fields = ('title', 'experiment', 'start', 'position', 'subj_restraint', 'subj_anesthesia_sedation')
    tabbed = True
    tab_name = 'Sessions'
    template = 'admin/tabular_view_session_grouped.html'

class TrialViewInline(FeedTabularInline):
    model = Trial
    extra = 0
    fields = ('position', 'session', 'title', 'food_type', 'behaviorowl_primary')
    tabbed = True
    tab_name="Trials"
    template = 'admin/tabular_view_trial_grouped.html'


class SubjectViewInline(FeedTabularInline):
    model = Subject
    extra = 0
    tabbed = True
    tab_name="Subjects"
    template = 'admin/tabular_view.html'

class StudyAdmin(FeedModelAdmin):
    inlines = (StudyPrivateInline,)
    view_inlines = [SubjectViewInline, ExperimentViewInline, SessionViewInline, TrialViewInline]
    search_fields = ('title', 'description')
    list_display = ('title','start','end', 'funding_agency',)
    # exclude old "approval" field
    exclude = ('approval',)
    form = StudyChangeForm
    tabbed = False

class ExperimentAdmin(FeedModelAdmin):
    inlines = [IllustrationInline]
    view_inlines = [IllustrationViewInline]
    search_fields = ('title','study__title','subject__taxon__genus','subject__taxon__species','subject__taxon__common_name','subject__name','description','subject_notes','impl_notes')
    list_display = ('title','study', 'subject','subj_devstage')
    form = ExperimentChangeForm
    fields = ('setup_types', 'title', 'bookkeeping', 'subject', 'start', 'end', 'description', 'subj_devstage', 'subj_age', 'subj_ageunit', 'subj_weight', 'subj_tooth', 'subject_notes', 'impl_notes',)
    #list_filter = ('study', 'subject')

class SubjectAdmin(FeedModelAdmin):
    inlines = [IllustrationInline]
    view_inlines = [IllustrationViewInline]
    search_fields = ('name','study__title', 'breed','taxon__species', 'taxon__genus','taxon__common_name','source','sex','notes')
    list_display = ('name', 'study', 'taxon', 'breed','sex', 'source')
    #list_filter = ('study', 'taxon','sex')
    exclude = ('study',)
    ordering = ('name',)
    form = DisableForeignKeyForm

class TrialAdmin(FeedModelAdmin):
    search_fields = ('title','bookkeeping','subj_notes','subj_treatment','food_type','food_property','behavior_primary__label','behavior_secondary','behavior_notes')
    list_display = ('title', 'session', 'taxon_name','food_type', 'behaviorowl_primary','waveform_picture')
    form = TrialChangeForm
    # hide old non-OWL behavior fields, hide dependent container references
    exclude = ('behavior_primary', 'behavior_secondary', 'experiment', 'study',)
    ordering = ('position',)

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
    template = 'admin/tabular_view.html'

class EmgSensorInline(FeedTabularInline):
    model = EmgSensor
    exclude = ['study', 'location_controlled', 'location_freetext']
    extra = 5
    form = EmgSensorChannelForm
    formset = OrderedFormset

class SonoSensorInline(SetupTabularInline):
    model = SonoSensor
    extra = 4
    exclude = ['study', 'location_controlled', 'location_freetext']
    form = SonoSensorForm

class SonoSensorViewInline(FeedTabularInline):
    model = SonoSensor
    extra = 0
    exclude = ['study', 'location_controlled', 'location_freetext']
    form = SonoSensorForm
    template = 'admin/tabular_view.html'

class StrainSensorInline(SetupTabularInline):
    model = StrainSensor
    extra = 3
    exclude = ['study']
    form = StrainSensorForm

class StrainSensorViewInline(FeedTabularInline):
    model = StrainSensor
    extra = 0
    exclude = ['study']
    form = StrainSensorForm
    template = 'admin/tabular_view.html'

class ForceSensorInline(SetupTabularInline):
    model = ForceSensor
    extra = 3
    exclude = ['study']
    form = ForceSensorForm

class ForceSensorViewInline(FeedTabularInline):
    model = ForceSensor
    extra = 0
    exclude = ['study']
    form = ForceSensorForm
    template = 'admin/tabular_view.html'

class PressureSensorInline(SetupTabularInline):
    model = PressureSensor
    extra = 3
    form = PressureSensorForm

class PressureSensorViewInline(FeedTabularInline):
    model = PressureSensor
    extra = 0
    exclude = ['study']
    form = PressureSensorForm
    template = 'admin/tabular_view.html'

class KinematicsSensorInline(SetupTabularInline):
    model = KinematicsSensor
    extra = 3
    exclude = ['study']
    form = KinematicsSensorForm

class KinematicsSensorViewInline(FeedTabularInline):
    model = KinematicsSensor
    extra = 0
    exclude = ['study']
    form = KinematicsSensorForm
    template = 'admin/tabular_view.html'

class ChannelInline(FeedTabularInline):
    model = Channel
    exclude = ['notes']
    extra = 0



class SonoChannelInline(FeedTabularInline):
    model = SonoChannel
    extra =5
    exclude = ['study']
    form = SonoChannelForm

class SonoChannelViewInline(FeedTabularInline):
    model = SonoChannel
    exclude = ['study']
    extra = 0
    template = 'admin/tabular_view.html'

class StrainChannelInline(FeedTabularInline):
    model = StrainChannel
    extra =9
    exclude = ['study']
    form = StrainChannelForm

class StrainChannelViewInline(FeedTabularInline):
    model = StrainChannel
    exclude = ['study']
    extra = 0
    template = 'admin/tabular_view.html'

class ForceChannelInline(FeedTabularInline):
    model = ForceChannel
    extra =9
    exclude = ['study']
    form = ForceChannelForm

class ForceChannelViewInline(FeedTabularInline):
    model = ForceChannel
    exclude = ['study']
    extra = 0
    template = 'admin/tabular_view.html'

class PressureChannelInline(FeedTabularInline):
    model = PressureChannel
    extra =9
    exclude = ['study']
    form = PressureChannelForm

class PressureChannelViewInline(FeedTabularInline):
    model = PressureChannel
    exclude = ['study']
    extra = 0
    template = 'admin/tabular_view.html'

class KinematicsChannelInline(FeedTabularInline):
    model = KinematicsChannel
    extra =9
    exclude = ['study']
    form = KinematicsChannelForm

class KinematicsChannelViewInline(FeedTabularInline):
    model = KinematicsChannel
    exclude = ['study']
    extra = 0
    template = 'admin/tabular_view.html'

class EventChannelInline(FeedTabularInline):
    model = EventChannel
    extra =9
    exclude = ['study']
    form = EventChannelForm

class EventChannelViewInline(FeedTabularInline):
    model = EventChannel
    exclude = ['study']
    extra = 0
    template = 'admin/tabular_view.html'

class OtherChannelInline(FeedTabularInline):
    model = OtherChannel
    extra =9
    exclude = ['study']
    form = OtherChannelForm

class OtherChannelViewInline(FeedTabularInline):
    model = OtherChannel
    exclude = ['study']
    extra = 0
    template = 'admin/tabular_view.html'

class EmgSetupAdmin(EmgSetupModelAdmin):
    inlines = [ IllustrationInline, EmgSensorInline]
    view_inlines = [IllustrationViewInline, EmgSensorViewInline]
    list_display = ('preamplifier','experiment')
    list_filter = ('experiment',)
    ordering = ('preamplifier',)
    exclude = ('study', 'experiment', 'technique')
    form = SetupForm

class SonoSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,SonoSensorInline,SonoChannelInline]
    view_inlines = [IllustrationViewInline, SonoSensorViewInline, SonoChannelViewInline]
    list_display = ('sonomicrometer','experiment')
    list_filter = ('experiment',)
    ordering = ('sonomicrometer',)
    exclude = ('study', 'experiment', 'technique')
    form = SetupForm

class StrainSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,StrainSensorInline,StrainChannelInline]
    view_inlines = [IllustrationViewInline, StrainSensorViewInline, StrainChannelViewInline]
    list_display = ('experiment',)
    list_filter = ('experiment',)
    exclude = ('study', 'experiment', 'technique')
    form = SetupForm

class ForceSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,ForceSensorInline,ForceChannelInline]
    view_inlines = [IllustrationViewInline, ForceSensorViewInline, ForceChannelViewInline]
    list_display = ('experiment',)
    list_filter = ('experiment',)
    exclude = ('study', 'experiment', 'technique')
    form = SetupForm

class PressureSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,PressureSensorInline,PressureChannelInline]
    view_inlines = [IllustrationViewInline, PressureSensorViewInline, PressureChannelViewInline]
    list_display = ('experiment',)
    list_filter = ('experiment',)
    exclude = ('study', 'experiment', 'technique')

class KinematicsSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,KinematicsSensorInline,KinematicsChannelInline]
    view_inlines = [IllustrationViewInline, KinematicsSensorViewInline, KinematicsChannelViewInline]
    list_display = ('experiment',)
    list_filter = ('experiment',)
    exclude = ('study', 'experiment')
    exclude = ('study', 'experiment', 'technique')
    form = SetupForm

class EventSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,EventChannelInline]
    view_inlines = [IllustrationViewInline, EventChannelViewInline]
    list_display = ('experiment',)
    list_filter = ('experiment',)
    exclude = ('study', 'experiment', 'technique')
    form = SetupForm

class OtherSetupAdmin(DefaultModelAdmin):
    inlines = [ IllustrationInline,OtherChannelInline]
    view_inlines = [IllustrationViewInline, OtherChannelViewInline]
    list_display = ('experiment',)
    list_filter = ('experiment',)
    exclude = ('study', 'experiment', 'technique')
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
    template = 'admin/tabular_view.html'

class SessionAdmin(SessionModelAdmin):
    inlines = [ChannelLineupInline]
    view_inlines = [ChannelLineupViewInline, TrialViewInline ]
    list_display = ('title', 'experiment','position', 'start', 'subj_restraint','subj_anesthesia_sedation')
    search_fields = ('title','bookkeeping','experiment__title','subj_notes','subj_restraint__label','subj_anesthesia_sedation')
    ordering = ('position',)
    exclude = ('study','experiment')
    form = SessionChangeForm
    tabbed = True
    tab_name = "Session"

class EmgSensorAdmin(EmgSensorModelAdmin):
    form = EmgSensorChannelForm

class SonoSensorAdmin(DefaultModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('setup','name', 'muscle', 'loc_side', 'loc_ap', 'loc_dv', 'loc_pd', 'loc_ml', 'notes')
        }),
    )
    ordering = ('name', 'muscle',)

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

class FeedUserProfileInline(FeedStackedInline):
    model = FeedUserProfile
    extra = 0

class FeedUserAdmin(UserAdmin):
    # disable "fancy" two-select widget for multiple-select fields
    filter_horizontal = ()
    inlines = [FeedUserProfileInline]

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
admin.site.register(OtherSetup,OtherSetupAdmin)
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
admin.site.register(OtherChannel, DefaultModelAdmin)
