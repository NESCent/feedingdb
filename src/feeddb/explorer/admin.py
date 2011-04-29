from django.contrib import admin 
from feeddb.feed import models as feedmodels
from feeddb.explorer.models import * 


# TODO: comment that this admin if exclusively for internal purposes

class TrialInBucketInline(admin.StackedInline):
    model = TrialInBucket

class BucketAdmin(admin.ModelAdmin):
    inlines = [ TrialInBucketInline ] 


admin.site.register(Bucket, BucketAdmin)

