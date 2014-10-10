from haystack.indexes import SearchIndex, Indexable, CharField, DateTimeField, MultiValueField
from feeddb.feed.models import Study, Subject, Experiment, Trial, Session, Techniques
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

def trial_muscles(obj):
    """
    Iterate over all EMG and Sono channels attached to a trial, yielding
    MuscleOwls
    """
    for channel in obj.session.channels.all():
        if hasattr(channel, 'emgchannel'):
            yield channel.emgchannel.sensor.muscle
        if hasattr(channel, 'sonochannel'):
            yield channel.sonochannel.crystal1.muscle
            yield channel.sonochannel.crystal2.muscle

CHANNEL_TYPES_HAVING_LOCATION_FREETEXT = (
    'strainchannel',
    'forcechannel',
    'pressurechannel',
    'kinematicschannel',
)

def trial_analocs(obj):
    """
    Iterate over all channels having 'location_freetext" field which are
    attached to a trial, yielding AnatomicalLocations
    """
    for channel in obj.session.channels.all():
        for channeltype in CHANNEL_TYPES_HAVING_LOCATION_FREETEXT:
            if hasattr(channel, channeltype):
                typedchannel = getattr(channel, channeltype)
                yield typedchannel.sensor.location_freetext

def fail_with_return_value(ret):
    def wrap(f):
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                return ret
        return wrapped
    return wrap

def unicodeify_list(f):
    def wrapped(*args, **kwargs):
        return [unicode(thing) for thing in f(*args, **kwargs)]
    return wrapped


class TrialIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)

    title = CharField(model_attr='title')
    session_title = CharField(model_attr='session__title')
    experiment_title = CharField(model_attr='session__experiment__title')
    study_title = CharField(model_attr='session__experiment__study__title')

    taxon = CharField(model_attr='session__experiment__subject__taxon', faceted=True)

    #accession = CharField(model_attr='accession', null=True)
    food_type = CharField(model_attr='food_type', null=True, faceted=True)
    food_size = CharField(model_attr='food_size', null=True)
    food_property = CharField(model_attr='food_property', null=True)

    created_at = DateTimeField(model_attr='created_at')
    updated_at = DateTimeField(model_attr='updated_at')

    behaviorowl_primary = CharField(model_attr='behaviorowl_primary', null=True)
    behaviorowl_primary_ancestors = MultiValueField(faceted=True)
    behaviorowl_primary_part_of = MultiValueField(faceted=True)

    techniques = MultiValueField(indexed=False, stored=True, faceted=True)

    # List of muscle labels for EMG and Sono sensors and non-muscle anatomical
    # locations on other sensors
    analoc_direct = MultiValueField()

    # `analoc_direct` along with the ancestors of each MuscleOwl in the list
    analoc = MultiValueField(faceted=True)

    # Muscles which members of `analoc_direct` are a part of, except when the same
    # muscle is already listed in `analoc`
    #
    # This is currently just muscles, but could be extended to include any
    # other OwlTerms if they are added later.
    analoc_part_of = MultiValueField(faceted=True)

    def prepare_techniques(self, obj):
        technique_dict = dict(Techniques.CHOICES)
        techniques = set()
        for channel in obj.session.channels.all():
            try:
                techniques.add(technique_dict[channel.setup.technique])
            except IndexError:
                print "Unknown technique #%d for channel %s on trial %s" % (
                    channel.setup.technique, channel, obj)

        if settings.DEBUG:
            print "Techniques: %s" % sorted(techniques)
        return sorted(techniques)

    @fail_with_return_value([])
    #@unicodeify_list
    def prepare_behaviorowl_primary_ancestors(self, obj):
        # TODO: should we be including the original behaviorowl here?
        return obj.behaviorowl_primary.ancestor_classes_inclusive()

    @fail_with_return_value([])
    #@unicodeify_list
    def prepare_behaviorowl_primary_part_of(self, obj):
        # TODO: should we be including the original behaviorowl here?
        return obj.behaviorowl_primary.part_of_classes_inclusive()

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

        muscles_ancestors = set()
        muscles_part_of = set()
        muscles_direct = set()
        for m in trial_muscles(obj):
            if m != None and len(unicode(m)):
                muscles_direct.add(unicode(m))
                for m_ancestor in m.ancestor_classes():
                    muscles_ancestors.add(unicode(m_ancestor))
                for m_part_of in m.part_of_classes():
                    muscles_part_of.add(unicode(m_part_of))

        muscles_part_of = muscles_part_of.difference(muscles_ancestors)

        self.prepared_data = super(TrialIndex, self).prepare(obj)
        if settings.DEBUG:
            print "MUSCLES DIRECT %s" % muscles_direct
            print "MUSCLES ANCESTORS %s" % muscles_ancestors
            print "MUSCLES PART OF %s" % muscles_part_of

        # Now add the anatomical location terms to the set
        analocs_direct = set()
        for al in trial_analocs(obj):
            if al != None and len(unicode(al)):
                analocs_direct.add(unicode(al))

        # Store all AnatomicalLocations, MuscleOwls, and ancestors of MuscleOwls
        self.prepared_data['analoc'] = list(analocs_direct | muscles_direct | muscles_ancestors)

        # Store muscles that the muscle is part of, but isn't already a
        # subclass of. We don't have "part_of" relationships for analocs, so
        # don't include them.
        self.prepared_data['analoc_part_of'] = list(muscles_part_of - muscles_ancestors)

        # Store MuscleOwls and AnatomicalLocations applied directly to the
        # trial's session's channel's sensors.
        self.prepared_data['analoc_direct'] = list(muscles_direct | analocs_direct)
        return self.prepared_data

    def load_all_queryset(self):
        return Trial.objects.all().prefetch_related('bucket_set')

    def get_model(self):
        return Trial
