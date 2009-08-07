from feeddb.feed.models import *
from django.contrib import admin
from django import forms
from feeddb.feed.extension.modeladmin import FeedModelAdmin, FeedTabularInline

class StudyPrivateInline(admin.StackedInline):
    model = StudyPrivate
    extra = 1
    max_num = 1

class ExperimentInline(FeedTabularInline):
    model = Experiment
    extra = 0
    fields = ['bookkeeping','accession','subject']

class SensorInline(FeedTabularInline):
    model = Sensor
    extra = 0
    fields = ['name','technique']

class SessionInline(FeedTabularInline):
    model = Session
    extra = 0
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
    class Meta:
        verbose_name = "emgsetup"

class SonoSetupInline(FeedTabularInline):
    model = SonoSetup
    extra = 0
    class Meta:
        verbose_name = "sonosetup"

class TrialInline(FeedTabularInline):
    model = Trial
    extra = 0
    fields = ['position', 'accession','claimed_duration','bookkeeping','behavior_primary','food_type']

class SubjectInline(FeedTabularInline):
    model = Subject
    extra = 0

class SubjectStackInline(admin.StackedInline):
    model = Subject
    extra = 1

class StudyAdmin(FeedModelAdmin):
    inlines = [StudyPrivateInline]
    view_inlines = [SubjectInline, ExperimentInline]
    search_fields = ('name',)
    list_display = ('name','accession','start','end','bookkeeping', 'funding_agency','approval_secured')

class ExperimentAdmin(FeedModelAdmin):
    inlines = [IllustrationInline]
    view_inlines = [IllustrationViewInline, EmgSetupInline, SonoSetupInline,SessionInline]
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

class EmgSensorInline(FeedTabularInline):
    model = EmgSensor
    excludes = ['notes']   
    extra = 0

class SonoSensorInline(FeedTabularInline):
    model = SonoSensor
    excludes = ['notes']   
    extra = 0

class ChannelInline(FeedTabularInline):
    model = Channel
    excludes = ['notes']   
    extra = 0


class EmgChannelInline(FeedTabularInline):
    model = EmgChannel
    excludes = ['notes']   
    extra = 0


class SonoChannelInline(FeedTabularInline):
    model = SonoChannel
    excludes = ['notes']   
    extra = 0

class EmgSetupAdmin(FeedModelAdmin):
    inlines = [ IllustrationInline]
    view_inlines = [IllustrationViewInline, EmgSensorInline, EmgChannelInline]
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

class ChannelLineupViewInline(FeedTabularInline):
    model = ChannelLineup
    extra = 0 


class SessionAdmin(FeedModelAdmin):
    inlines = [ChannelLineupInline]
    view_inlines = [ChannelLineupViewInline, TrialInline ]
    search_fields = ('accession', 'bookkeeping','subj_restraint','subj_anesthesia_sedation','subj_notes')
    list_display = ('position', 'bookkeeping', 'accession', 'experiment','start', 'end','subj_restraint','subj_anesthesia_sedation')
    list_filter = ('experiment', 'subj_restraint')
    ordering = ('position',)

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
