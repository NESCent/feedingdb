from haystack import indexes
from feeddb.feed.models import Study, Subject, Experiment

class SubjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #taxon = models.
    name = indexes.CharField(model_attr='name')
    breed = indexes.CharField(model_attr='breed', faceted=True)
    sex = indexes.CharField(model_attr='sex', null=True, faceted=True)
    taxon = indexes.CharField(faceted=True)

    def prepare_taxon(self, obj):
        return "%s" % str(obj.taxon)
    
    def prepare_taxon_exact(self, obj):
        return obj.taxon.id

    def get_model(self):
        return Subject

    #def index_queryset(self, using=None):
