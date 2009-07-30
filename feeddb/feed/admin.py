from feeddb.feed.models import *
from django.contrib import admin

class StudyPrivateInline(admin.StackedInline):
    model = StudyPrivate
    extra = 1
    max_num = 1

class ExperimentInline(admin.TabularInline):
    model = Experiment
    extra = 0
    fields = ['bookkeeping','accession','subject']

class SensorInline(admin.TabularInline):
    model = Sensor
    extra = 0
    fields = ['name','muscle','side']

class SessionInline(admin.TabularInline):
    model = Session
    extra = 0
    excludes = ['subj_notes']

class TrialInline(admin.TabularInline):
    model = Trial
    extra = 0
    fields = ['position', 'accession','claimed_duration','bookkeeping','behavior_primary','food_type']

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 0

class StudyAdmin(admin.ModelAdmin):
    inlines = [StudyPrivateInline]
    view_inlines = [ExperimentInline,SubjectInline]
    search_fields = ('name',)
    list_display = ('name','accession','start','end','bookkeeping', 'funding_agency','approval_secured', 'view')
    list_display_links = ('name', 'view')

class ExperimentAdmin(admin.ModelAdmin):
    view_inlines = [SensorInline, SessionInline]
    search_fields = ('decription',)
    list_display = ('subject','study','start','end','bookkeeping', 'subj_devstage','subj_tooth', 'view')
    list_display_links = ('bookkeeping', 'view',)
    list_filter = ('study', 'subject')
    
class SessionAdmin(admin.ModelAdmin):
    view_inlines = [TrialInline]
    search_fields = ('accession', 'bookkeeping')

class TrialAdmin(admin.ModelAdmin):
    search_fields = ('accession', 'bookkeeping','behavior_primary', 'food_type')
    list_display = ('position', 'accession', 'bookkeeping','behavior_primary', 'food_type','food_size', 'session','view')
    list_display_links = ('position','view')
    list_filter = ('behavior_primary', 'food_type','session')
    ordering = ('position',)

class TaxonAdmin(admin.ModelAdmin):
    mdel = Taxon
    prepopulated_fields = {"label": ("genus","species", )}



admin.site.register(Technique)	
admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Muscle)
admin.site.register(Side)
admin.site.register(DepthAxis)
admin.site.register(AnteriorPosteriorAxis)
admin.site.register(DorsalVentralAxis)
admin.site.register(EletrodeType)
admin.site.register(DevelopmentStage)
admin.site.register(Behavior)
admin.site.register(Restraint)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Subject)
admin.site.register(Sensor)
admin.site.register(Study,StudyAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Trial,TrialAdmin)


