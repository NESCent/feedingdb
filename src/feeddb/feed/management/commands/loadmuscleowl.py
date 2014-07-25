from django.core.management.base import BaseCommand, CommandError
from feeddb.feed.models import MuscleOwl

# first draft of command to import muscle terms from an OWL file
class Command(BaseCommand):
    args = '<file>'
    help = 'help'

    def handle(self, *args, **options):
        from rdflib.graph import Graph
        from rdflib import RDFS
        from rdflib.term import URIRef, BNode, Literal
        import yaml

        print yaml.dump(args)
        OboDefinition = URIRef('http://purl.obolibrary.org/obo/IAO_0000115')

        g = Graph()
        g.parse(args[0], 'xml')

        # first pass, add the muscles
        subjects = set(g.subjects())
        for subject in subjects:
            if isinstance(subject, BNode):
                continue

            slabel = g.label(subject)
            if len(slabel):
                m = MuscleOwl()
                m.uri = unicode(subject)
                m.label = unicode(slabel)
                m.obo_definition = unicode(g.value(subject, OboDefinition, None))
                m.rdfs_comment = unicode(g.value(subject, RDFS.comment, None))
                m.save()

        # second pass, add the relationships
        for subject in subjects:
            if isinstance(subject, BNode):
                continue
                
            slabel = g.label(subject)
            if len(slabel):
                m = MuscleOwl.objects.get(uri=unicode(subject))
                tobjs = g.transitive_objects(subject, RDFS.subClassOf)
                for obj in g.transitive_objects(subject, RDFS.subClassOf):
                    if isinstance(obj, BNode):
                        continue

                    print unicode(obj)
                    a = MuscleOwl.objects.get(uri=unicode(obj))
                    m.rdfs_subClassOf_ancestors.add(a)

                m.save()
