from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from invapp.models import Collection, Project, Item
from invapp import utils


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-i', '--item', dest='ipk', default=None, metavar='ID',
            help='Update an item with id=ID,' + \
                ' or update all items if no id passed'),
        make_option('-p', '--project', dest='ppk', default=None, metavar='ID',
            help='Update a project with id=ID,' + \
                ' or update all projects if no id passed'),
        make_option('-c', '--collection', dest='cpk', default=None,
            metavar='ID', help='Update a collection with id=ID,' + \
                ' or update all collections if no id passed')        
        )

    help = '''Update stats for one or all objects belonging to a class.
Works with Item, Project, or Collection.
To update entire system pass no options.
If an Item and Proj or Coll are specified, Item will always be updated first
'''

    def handle(self, *args, **options):
        if args:
            raise CommandError('No args should be passed to this command')
        if not options:
            self.report(utils.update_all_stats())
        errors = []
        if options.item:
            if options.ipk:
                errors += utils.update_object_stats(Item, ipk)
            else:
                errors += utils.update_model_stats(Item)
        if options.project:
            if options.ppk:
                errors += utils.update_object_stats(Project, ipk)
            else:
                errors += utils.update_model_stats(Project)
        if options.collection:
            if options.cpk:
                errors += utils.update_object_stats(Collection, ipk)
            else:
                errors += utils.update_model_stats(Collection)
        self.report(errors)

    def report(self, errors):
        print 'Update process completed with %s errors' % len(errors)
        for e in errors:
            print e