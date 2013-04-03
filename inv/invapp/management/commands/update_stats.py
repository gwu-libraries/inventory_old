from optparse import make_option
from pprint import pprint

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from invapp.models import Collection, Project, Item
from invapp import utils


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        # single object options
        make_option('-i', '--item', dest='item', metavar='ID',
            help='Update stats for an item with id=ID,'),
        make_option('-p', '--project', dest='project', metavar='ID',
            help='Update stats for a project with id=ID,'),
        make_option('-c', '--collection', dest='collection', metavar='ID',
            help='Update stats for a collection with id=ID,'),
        # model level options
        make_option('-I', '--Items', dest='Items',
            action='store_true', help='Update all items\' stats'),
        make_option('-P', '--Projects', dest='Projects',
            action='store_true', help='Update all projects\' stats'),
        make_option('-C', '--Collections', dest='Collections',
            action='store_true', help='Update all collections\' stats'),
        # system option
        make_option('-A', '--All', dest='All', action='store_true',
            help='Update the entire system')
        )

    help = '''Update stats for one or all objects belonging to a class.
Works with Item, Project, or Collection.
To update entire system pass no options.
If an Item and Proj or Coll are specified, Item will always be updated first
'''

    def handle(self, *args, **options):
        if args:
            raise CommandError('No args used with this command, use options')
        errors = []
        if options['item']:
            print 'Updating Item with id=%s' % options['item']
            e = utils.update_object_stats_quietly(model=Item,
                id=options['item'])
            if e: errors.append(e)
            print 'Stats for item %s:' % options['item']
            pprint(Item.objects.get(id=options['item']).stats)
        if options['Items']:
            print 'Updating all Items'
            errors += utils.update_model_stats(Item)
        if options['project']:
            print 'Updating Project with id=%s' % options['project']
            e = utils.update_object_stats_quietly(model=Project,
                id=options['project'])
            if e: errors.append(e)
            print 'Stats for project %s:' % options['project']
            pprint(Project.objects.get(id=options['project']).stats)
        if options['Projects']:
            print 'Updating all Projects'
            errors += utils.update_model_stats(Project)
        if options['collection']:
            print 'Updating Collection with id=%s' % options['collection']
            e = utils.update_object_stats_quietly(model=Collection,
                id=options['collection'])
            if e: errors.append(e)
            print 'Stats for Collection %s:' % options['collection']
            pprint(Collection.objects.get(id=options['collection']).stats)
        if options['Collections']:
            print 'Updating all Collections'
            errors += utils.update_model_stats(Collection)
        if options['All']:
            print 'Updating entire system'
            errors += utils.update_all_stats()
        print 'Update process completed with %s errors' % len(errors)
        for e in errors:
            print e