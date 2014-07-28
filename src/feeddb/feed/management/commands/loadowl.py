from django.core.management.base import BaseCommand, CommandError
from feeddb.feed.models import MuscleOwl, BehaviorOwl

def nonblankthings(g, things):
    from rdflib.term import URIRef, BNode, Literal
    for thing in set(things):
        if isinstance(thing, BNode):
            continue

        label = g.label(thing)
        if len(label):
            yield thing

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

        g = Graph()
        g.parse(args[1], 'xml')

        Model = MuscleOwl if args[0] == 'm' else BehaviorOwl

        # first pass, add the things
        for subject in nonblankthings(g, g.subjects()):
            slabel = g.label(subject)
            m = Model()
            m.uri = unicode(subject)
            m.label = unicode(slabel)
            # FIXME: each subject can have multiple types, so this needs a helper function
            # to choose the best type. Or a multi-valued field (ugh).
            #m.rdf_type = unicode(g.value(subject, RDF.type, None))
            m.obo_definition = unicode(g.value(subject, OboDefinition, None))
            m.rdfs_comment = unicode(g.value(subject, RDFS.comment, None))
            m.save()

        # second pass, add the relationships
        for subject in nonblankthings(g, g.subjects()):
            slabel = g.label(subject)
            m = Model.objects.get(uri=unicode(subject))

            # add all super-classes to m.rdfs_subClassOf_ancestors
            for obj in nonblankthings(g, g.transitive_objects(subject, RDFS.subClassOf)):
                if obj != subject:
                    print unicode(obj)
                    a = Model.objects.get(uri=unicode(obj))
                    m.rdfs_subClassOf_ancestors.add(a)

            # add only direct super-classes to m.rdfs_subClassOf
            #for obj in nonblankthings(g, g.objects(subject, RDFS.subClassOf)):
            #    if obj != subject:
            #        a = Model.objects.get(uri=unicode(obj))
            #        m.rdfs_subClassOf.add(a)

            m.save()
