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

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 0

class StudyAdmin(admin.ModelAdmin):
    inlines = [StudyPrivateInline]
    view_inlines = [ExperimentInline,SubjectInline]
    search_fields = ['name']

class ExperimentAdmin(admin.ModelAdmin):
    view_inlines = [SensorInline]
    search_fields = ['decription']

admin.site.register(Technique)	
admin.site.register(Taxon)
admin.site.register(Muscle)
admin.site.register(Side)
admin.site.register(DepthAxis)
admin.site.register(AnteriorPosteriorAxis)
admin.site.register(DorsalVentralAxis)
admin.site.register(EletrodeType)
admin.site.register(DevelopmentStage)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Subject)
admin.site.register(Sensor)
admin.site.register(Study,StudyAdmin)

