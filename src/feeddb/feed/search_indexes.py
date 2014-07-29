from haystack.indexes import SearchIndex, Indexable, CharField, DateTimeField, MultiValueField
from feeddb.feed.models import Study, Subject, Experiment, Trial, Session

class TrialIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)

    title = CharField(model_attr='title')
    session_title = CharField(model_attr='session__title')
    experiment_title = CharField(model_attr='session__experiment__title')
    study_title = CharField(model_attr='session__experiment__study__title')

    #accession = CharField(model_attr='accession', null=True)
    food_type = CharField(model_attr='food_type', null=True)
    food_size = CharField(model_attr='food_size', null=True)
    food_property = CharField(model_attr='food_property', null=True)

    created_at = DateTimeField(model_attr='created_at')
    updated_at = DateTimeField(model_attr='updated_at')

    #behavior_primary = CharField(model_attr='behavior_primary')
    #behaviors_expanded = MultiValueField()

    muscles = MultiValueField(faceted=True)

    def prepare_muscles(self, obj):
        """
        Prepare the list of muscles for the index by traversing all channels on
        this trial and including all muscles listed on channels which include a
        muscle term. These channels are just EMG and Sono types.
        """

        def trial_muscles(obj):
            for channel in obj.session.channels.all():
                if hasattr(channel, 'emgchannel'):
                    yield channel.emgchannel.sensor.muscle
                if hasattr(channel, 'sonochannel'):
                    for m in [channel.sonochannel.crystal1.muscle, channel.sonochannel.crystal2.muscle]:
                        yield m

        muscles = set()
        for m in trial_muscles(obj):
            if m != None and len(unicode(m)):
                muscles.add(unicode(m))
                for m_ancestor in m.rdfs_subClassOf_ancestors.all():
                    muscles.add(unicode(m_ancestor))

        print "MUSCLES %s" % muscles
        return list(muscles) if len(muscles) else None

    def get_model(self):
        return Trial
