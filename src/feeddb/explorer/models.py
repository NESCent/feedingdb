from django.db import models
from feeddb.feed import models as feedmodels

# Create your models here.

class Bucket(feedmodels.FeedBaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    trials = models.ManyToManyField(feedmodels.Trial, through='TrialInBucket')

    def __unicode__(self):
        return self.title


class TrialInBucket(models.Model):
    trial = models.ForeignKey(feedmodels.Trial)
    bin = models.ForeignKey(Bucket)


