from django.core.management.base import BaseCommand, CommandError
from feeddb.feed.models import MuscleOwl, BehaviorOwl
import pprint

def nonblankthings(g, things):
    from rdflib.term import URIRef, BNode, Literal
    for thing in set(things):
        if isinstance(thing, BNode):
            continue

        label = g.label(thing)
        if len(label):
            yield thing

def get_model_instance(Model, uri):
    """
    Get an instance of the specified model, identified by the specified uri.

    If the instance can't be found, create a new one.
    """
    try:
        m = Model.objects.get(uri=uri)
    except Model.DoesNotExist:
        print "NEW: %s" % uri
        m = Model()
        m.uri = uri
    return m

# first draft of command to import muscle terms from an OWL file
class Command(BaseCommand):
    args = '<file>'
    help = 'help'

    def handle(self, *args, **options):
        from rdflib.graph import Graph
        from rdflib import RDFS, RDF, OWL
        from rdflib.term import URIRef, BNode, Literal
        import yaml

        OboDefinition = URIRef('http://purl.obolibrary.org/obo/IAO_0000115')
        part_of_some = URIRef('http://purl.obolibrary.org/obo/BFO_0000050_some')
        Synonym = URIRef(u'http://www.geneontology.org/formats/oboInOwl#hasSynonym')

        g = Graph()
        g.parse(args[1], 'xml')

        Model = MuscleOwl if args[0] == 'm' else BehaviorOwl

        # first pass, add the things
        for subject in nonblankthings(g, g.subjects()):
            slabel = g.label(subject)
            m = get_model_instance(Model, unicode(subject))
            m.uri = unicode(subject)
            m.label = unicode(slabel)

            m.rdfs_is_class = (subject, RDF.type, OWL.Class) in g
            m.obo_definition = unicode(g.value(subject, OboDefinition, None))
            m.rdfs_comment = unicode(g.value(subject, RDFS.comment, None))
            synonyms = [unicode(syn) for syn in g.objects(subject, Synonym)]
            if len(synonyms):
                m.synonyms_comma_separated = ", ".join(synonyms)
            else:
                m.synonyms_comma_separated = None

            m.save()

        # second pass, add the relationships
        for subject in nonblankthings(g, g.subjects()):
            slabel = g.label(subject)
            m = Model.objects.get(uri=unicode(subject))

            m.rdfs_subClassOf_ancestors.clear()
            # add all super-classes to m.rdfs_subClassOf_ancestors
            for obj in nonblankthings(g, g.transitive_objects(subject, RDFS.subClassOf)):
                if obj != subject:
                    a = Model.objects.get(uri=unicode(obj))
                    m.rdfs_subClassOf_ancestors.add(a)

            m.bfo_part_of_some.clear()
            # add all things that this thing is part of to m.bfo_part_of_some
            for obj in nonblankthings(g, g.objects(subject, part_of_some)):
                if obj != subject:
                    a = Model.objects.get(uri=unicode(obj))
                    m.bfo_part_of_some.add(a)

            # add only direct super-classes to m.rdfs_subClassOf
            #for obj in nonblankthings(g, g.objects(subject, RDFS.subClassOf)):
            #    if obj != subject:
            #        a = Model.objects.get(uri=unicode(obj))
            #        m.rdfs_subClassOf.add(a)

            m.save()
