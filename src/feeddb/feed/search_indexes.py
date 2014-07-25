from haystack.indexes import SearchIndex, Indexable, CharField, DateTimeField, MultiValueField
from feeddb.feed.models import Study, Subject, Experiment, Trial, Session

class SubjectIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)

    #taxon = models.
    name = CharField(model_attr='name')
    breed = CharField(model_attr='breed', faceted=True)
    sex = CharField(model_attr='sex', null=True, faceted=True)
    taxon = CharField(faceted=True)

    def prepare_taxon(self, obj):
        return "%s" % str(obj.taxon)
    
    def prepare_taxon_exact(self, obj):
        return obj.taxon.id

    def get_model(self):
        return Subject

    #def index_queryset(self, using=None):

class TrialIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)

    accession = CharField(model_attr='accession', null=True)
    food_type = CharField(model_attr='food_type', null=True)
    food_size = CharField(model_attr='food_size', null=True)
    food_property = CharField(model_attr='food_property', null=True)

    created_at = DateTimeField(model_attr='created_at')
    updated_at = DateTimeField(model_attr='updated_at')

    behavior_primary = CharField(model_attr='behavior_primary')
    behaviors_expanded = MultiValueField()

    def prepare_behaviors_expanded(self, obj):
        return ['qwer', 'tyui']

    def get_model(self):
        return Trial
