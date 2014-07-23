from haystack import indexes
from feeddb.feed.models import Study, Subject, Experiment

class SubjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #taxon = models.
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Subject

    #def index_queryset(self, using=None):
