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

    # List of muscle labels for EMG and Sono sensors
    muscles_direct = MultiValueField()

    # `muscles_direct` along with each muscle's ancestors
    muscles = MultiValueField(faceted=True)

    # Muscles which members of `muscles_direct` are a part of, except when the same
    # muscle is already listed in `muscles`
    muscles_part_of = MultiValueField(faceted=True)

    def prepare(self, obj):
        """
        Prepare the list of muscles for the index by traversing all channels on
        this trial and including all muscles listed on channels which include a
        muscle term. These channels are just EMG and Sono types.

        We also prepare the list of muscles which have the target muscle as a
        part, but only store the muscles which are distinct from the muscles we
        are already storing in the subClassOf field.

        This arrangement enables a search to be broadened from just subClass
        relationships to both subClass and part_of relationships by adding an
        OR filter on the `muscles_part_of` field.  An alternate implemention
        might instead store two independent fields for indexing; one uses just
        the subClassOf relationship and the other might use both. A search
        would be broadened by switching from one field to the other.
        """

        def trial_muscles(obj):
            for channel in obj.session.channels.all():
                if hasattr(channel, 'emgchannel'):
                    yield channel.emgchannel.sensor.muscle
                if hasattr(channel, 'sonochannel'):
                    for m in [channel.sonochannel.crystal1.muscle, channel.sonochannel.crystal2.muscle]:
                        yield m

        muscles = set()
        muscles_part_of = set()
        muscles_direct = set()
        for m in trial_muscles(obj):
            if m != None and len(unicode(m)):
                muscles.add(unicode(m))
                muscles_direct.add(unicode(m))
                for m_ancestor in m.rdfs_subClassOf_ancestors.filter(rdfs_is_class=True):
                    muscles.add(unicode(m_ancestor))
                for m_part_of in m.bfo_part_of_some.filter(rdfs_is_class=True):
                    muscles_part_of.add(unicode(m_part_of))

        # Only store muscles that the muscle is part of, but isn't already a
        # subclass of
        muscles_part_of = muscles_part_of.difference(muscles)

        self.prepared_data = super(TrialIndex, self).prepare(obj)
        print "MUSCLES %s" % muscles
        print "MUSCLES PART OF %s" % muscles_part_of
        self.prepared_data['muscles'] = list(muscles) if len(muscles) else None
        self.prepared_data['muscles_part_of'] = list(muscles_part_of) if len(muscles_part_of) else None
        self.prepared_data['muscles_direct'] = list(muscles_direct) if len(muscles_direct) else None
        return self.prepared_data

    def get_model(self):
        return Trial
