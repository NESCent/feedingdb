from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed import models

class Command(BaseCommand):
    args = '<file>'
    help = 'help'

    def handle(self, *args, **options):
        broken = []
        valid = []
        qs = models.ChannelLineup.objects.all().prefetch_related('session', 'session__experiment', 'channel', 'channel__setup', 'channel__setup__experiment')
        for lineup in qs:
            session = lineup.session
            channel = lineup.channel
            if channel is not None:
                if session.experiment != channel.setup.experiment:
                    print "Broken!"
                    print "  Lineup pk={lineup.pk} '{lineup}'".format(lineup=lineup)
                    print "    Channel pk={channel.pk} '{channel}'".format(channel=channel)
                    print "      Setup pk={setup.pk} '{setup}'".format(setup=channel.setup)
                    print "        Experiment pk={exp.pk} '{exp}'".format(exp=channel.setup.experiment)
                    print "    Session pk={session.pk} '{session}'".format(session=session)
                    print "      Experiment pk={exp.pk} '{exp}'".format(exp=session.experiment)
                    print ""
                    broken.append(lineup)
                else:
                    valid.append(lineup)
                

        print "Total broken: %d" % len(broken)
        print "Total valid: %d" % len(valid)
