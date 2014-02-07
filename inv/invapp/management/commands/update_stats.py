from optparse import make_option
from pprint import pprint

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models.signals import post_save, post_delete

from invapp.models import Bag, Collection, Project, Item, \
    disconnect_signal, reconnect_signal, update_item_stats_receiver,\
    update_collection_stats_receiver
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
        # check for syntax errors
        if args:
            raise CommandError('Use options, not args with this command')
        # make sure at least one option passed
        stdopts = ['settings', 'pythonpath', 'verbosity', 'traceback']
        ovals = [options[o] for o in options if o not in stdopts]
        if not any(ovals):
            raise CommandError('No options passed')
        # begin processing
        errors = []
        if options['item']:
            print 'Updating Item with id=%s' % options['item']
            e = utils.update_object_stats_quietly(model=Item,
                                                  id=options['item'])
            if e:
                errors.append(e)
            print 'Stats for item %s:' % options['item']
            pprint(Item.objects.get(id=options['item']).stats)
        if options['Items']:
            print 'Updating all Items'
            errors += utils.update_model_stats(Item)
        if options['project']:
            print 'Updating Project with id=%s' % options['project']
            e = utils.update_object_stats_quietly(model=Project,
                                                  id=options['project'])
            if e:
                errors.append(e)
            print 'Stats for project %s:' % options['project']
            pprint(Project.objects.get(id=options['project']).stats)
        if options['Projects']:
            print 'Updating all Projects'
            errors += utils.update_model_stats(Project)
        if options['collection']:
            print 'Updating Collection with id=%s' % options['collection']
            e = utils.update_object_stats_quietly(model=Collection,
                                                  id=options['collection'])
            if e:
                errors.append(e)
            print 'Stats for Collection %s:' % options['collection']
            pprint(Collection.objects.get(id=options['collection']).stats)
        if options['Collections']:
            print 'Updating all Collections'
            errors += utils.update_model_stats(Collection)
        if options['All']:
            #Disconnect all signals
            disconnect_signal(post_save, update_item_stats_receiver,
                              sender=Bag)
            disconnect_signal(post_delete, update_item_stats_receiver,
                              sender=Bag)
            disconnect_signal(post_save, update_collection_stats_receiver,
                              sender=Item)
            disconnect_signal(post_delete, update_collection_stats_receiver,
                              sender=Item)

            print 'Updating entire system'
            errors += utils.update_all_stats()

            #Reconnect all signals
            reconnect_signal(post_save, update_item_stats_receiver,
                             sender=Bag)
            reconnect_signal(post_delete, update_item_stats_receiver,
                             sender=Bag)
            reconnect_signal(post_save, update_collection_stats_receiver,
                             sender=Item)
            reconnect_signal(post_delete, update_collection_stats_receiver,
                             sender=Item)
        print 'Update process completed with %s errors' % len(errors)
        for e in errors:
            print e
