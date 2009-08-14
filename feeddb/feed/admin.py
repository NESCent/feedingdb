from feeddb.feed.models import *
from django.contrib import admin
from django import forms
from django.forms import models
from feeddb.feed.extension.modeladmin import FeedModelAdmin, FeedTabularInline, SessionModelAdmin, ExperimentModelAdmin
from feeddb.feed.extension.forms import *

class StudyPrivateInline(admin.StackedInline):
    model = StudyPrivate
    extra = 1
    max_num = 1

class ExperimentInline(FeedTabularInline):
    model = Experiment
    extra = 1
    form = ExperimentForm
    tabbed = True
    tab_name = "Experiments"

class ExperimentViewInline(FeedTabularInline):
    model = Experiment
    extra = 0
    tabbed = True
    fields = ['bookkeeping','accession','subject','subj_devstage','subj_age', 'subj_weight', 'subj_tooth']
    tab_name = "Experiments"

class SensorInline(FeedTabularInline):
    model = Sensor
    extra = 0
    fields = ['name','technique']

class SessionInline(FeedTabularInline):
    model = Session
    extra = 1
    excludes = ['subj_notes']

class SessionViewInline(FeedTabularInline):
    model = Session
    extra = 0
    tab_name = "Sessions"
    tabbed = True
    excludes = ['subj_notes']

class IllustrationInline(FeedTabularInline):
    model = Illustration
    extra = 1
    fields = ('picture', 'notes')

class IllustrationViewInline(FeedTabularInline):
    model = Illustration
    extra = 0
    fields = ('picture', 'notes')

class EmgSetupInline(FeedTabularInline):
    model = EmgSetup
    extra = 0
    tab_name = "EMG"
    tabbed = True

    class Meta:
        verbose_name = "emgsetup"
        
class SonoSetupInline(FeedTabularInline):
    model = SonoSetup
    extra = 0
    tab_name = "Sono"
    tabbed = True
    class Meta:
        verbose_name = "sonosetup"

class TrialInline(admin.StackedInline):
    model = Trial
    extra = 1
    tabbed = True
    tab_name="Trials"

class TrialViewInline(FeedTabularInline):
    model = Trial
    extra = 0
    fields = ['position', 'accession','claimed_duration','bookkeeping','behavior_primary','food_type']
    tabbed = True
    tab_name="Trials"

class SubjectInline(FeedTabularInline):
    model = Subject
    extra = 1
    form = SubjectForm
    tabbed = True
    tab_name="Subjects"

class SubjectViewInline(FeedTabularInline):
    model = Subject
    extra = 2
    tabbed = True
    tab_name="Subjects"

class SubjectStackInline(admin.StackedInline):
    model = Subject
    extra = 1

class StudyAdmin(FeedModelAdmin):
    inlines = [StudyPrivateInline,SubjectInline, ExperimentInline]
    view_inlines = [SubjectViewInline, ExperimentViewInline]
    search_fields = ('name',)
    list_display = ('name','accession','start','end','bookkeeping', 'funding_agency','approval_secured')
    tabbed = True


class ExperimentAdmin(ExperimentModelAdmin):
    inlines = [IllustrationInline]
    view_inlines = [IllustrationViewInline]
    search_fields = ('decription',)
    list_display = ('subject','study','start','end','bookkeeping', 'subj_devstage','subj_tooth')
    list_filter = ('study', 'subject')



class SubjectAdmin(FeedModelAdmin):
    search_fields = ('name', 'breed','taxon', 'source','sex','notes')
    list_display = ('name', 'taxon', 'breed','sex', 'source')
    list_filter = ('study', 'taxon','sex')
    ordering = ('name',)

class TrialAdmin(FeedModelAdmin):
    search_fields = ('accession', 'bookkeeping','behavior_primary', 'food_type')
    list_display = ('position', 'accession', 'bookkeeping','behavior_primary', 'food_type','food_size', 'session')
    list_filter = ('behavior_primary', 'food_type','session')
    ordering = ('position',)

class IllustrationAdmin(FeedModelAdmin):
    search_fields = ('notes', 'experiment','setup', 'subject')
    list_display = ('picture', 'notes')
    list_filter = ('experiment', 'subject')
    ordering = ('picture',)


class EmgSensorViewInline(FeedTabularInline):
    model = EmgSensor
    excludes = ['notes']   
    extra = 0
    form = EmgSensorForm

class EmgSensorInline(FeedTabularInline):
    model = EmgSensor
    excludes = ['notes']   
    extra = 1
    form = EmgSensorForm

class SonoSensorInline(FeedTabularInline):
    model = SonoSensor
    excludes = ['notes']   
    extra = 0

class ChannelInline(FeedTabularInline):
    model = Channel
    excludes = ['notes']   
    extra = 0

class EmgChannelViewInline(FeedTabularInline):
    model = EmgChannel
    excludes = ['notes']   
    extra = 0


class EmgChannelInline(FeedTabularInline):
    model = EmgChannel
    excludes = ['notes']   
    extra = 1


class SonoChannelInline(FeedTabularInline):
    model = SonoChannel
    extra = 0

class EmgElectrodeInline(FeedTabularInline):
    model = EmgElectrode
    extra = 1    
    form = EmgElectrodeForm

class EmgElectrodeViewInline(FeedTabularInline):
    model = EmgElectrode
    excludes = ['notes']
    extra = 0 
    form = EmgElectrodeForm

class EmgSetupAdmin(FeedModelAdmin):
    inlines = [ IllustrationInline, EmgElectrodeInline]
    view_inlines = [IllustrationViewInline, EmgElectrodeViewInline]
    list_display = ('technique', 'preamplifier','experiment')
    list_filter = ('technique', 'experiment')
    ordering = ('preamplifier',)


class SonoSetupAdmin(FeedModelAdmin):
    inlines = [ IllustrationInline]
    view_inlines = [IllustrationViewInline, SonoSensorInline, SonoChannelInline]
    list_display = ('technique', 'sonomicrometer','experiment')
    list_filter = ('technique', 'experiment')
    ordering = ('sonomicrometer',)

class EmgChannelAdmin(FeedModelAdmin):
    list_display = ('name', 'rate', 'sensor','emg_unit', 'emg_filtering')
    ordering = ('sensor',)

class SonoChannelAdmin(FeedModelAdmin):
    list_display = ('name', 'rate', 'crystal1','crystal2','sono_unit')
    ordering = ('crystal1',)

class ChannelLineupInline(FeedTabularInline):
    model = ChannelLineup
    extra = 3    
    tabbed = True
    tab_name="Channel Lineups"

class ChannelLineupViewInline(FeedTabularInline):
    model = ChannelLineup
    extra = 0 
    tabbed = True
    tab_name="Channel Lineups"

class SessionAdmin(SessionModelAdmin):
    inlines = [ChannelLineupInline, TrialInline]
    view_inlines = [ChannelLineupViewInline, TrialViewInline ]
    search_fields = ('accession', 'bookkeeping','subj_restraint','subj_anesthesia_sedation','subj_notes')
    list_display = ('position', 'bookkeeping', 'accession', 'experiment','start', 'end','subj_restraint','subj_anesthesia_sedation')
    list_filter = ('experiment', 'subj_restraint')
    ordering = ('position',)
    tabbed = True
    tab_name = "Session"

class EmgSensorAdmin(FeedModelAdmin):
    list_display = ('name', 'muscle', 'side', 'axisdepth','axisap','axisdv','eletrode_type')
    ordering = ('name', 'muscle',)

class SonoSensorAdmin(FeedModelAdmin):
    list_display = ('name', 'muscle', 'side', 'axisdepth','axisap','axisdv')
    ordering = ('name', 'muscle',)

class ChannelLineupAdmin(FeedModelAdmin):
    list_display = ('position', 'session','channel')
    list_filter = ('session',)
    ordering = ('session','position',)

class TermAdmin(FeedModelAdmin):
    list_display = ('label', 'controlled','deprecated')
    list_filter = ('controlled','deprecated')
    ordering = ('label',)
    
class TaxonAdmin(FeedModelAdmin):
    list_display = ('genus','species','common_name', 'controlled','deprecated')
    list_filter = ('genus','controlled','deprecated')
    ordering = ('genus','species')

admin.site.register(Technique,TermAdmin)	
admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Muscle,TermAdmin)
admin.site.register(Side,TermAdmin)
admin.site.register(DepthAxis,TermAdmin)
admin.site.register(AnteriorPosteriorAxis,TermAdmin)
admin.site.register(DorsalVentralAxis,TermAdmin)
admin.site.register(EletrodeType,TermAdmin)
admin.site.register(DevelopmentStage,TermAdmin)
admin.site.register(Behavior,TermAdmin)
admin.site.register(Restraint,TermAdmin)
admin.site.register(Emgunit,TermAdmin)
admin.site.register(Sonounit,TermAdmin)
admin.site.register(Emgfiltering,TermAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Sensor)
admin.site.register(Study,StudyAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Trial,TrialAdmin)
admin.site.register(EmgSetup,EmgSetupAdmin)
admin.site.register(SonoSetup,SonoSetupAdmin)
admin.site.register(EmgSensor, EmgSensorAdmin)
admin.site.register(SonoSensor, SonoSensorAdmin)
admin.site.register(ChannelLineup, ChannelLineupAdmin)
admin.site.register(Illustration,IllustrationAdmin)
admin.site.register(EmgChannel,EmgChannelAdmin)
admin.site.register(SonoChannel,SonoChannelAdmin)
admin.site.register(Channel)
