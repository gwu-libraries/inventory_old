import os, csv, re
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc, make_aware
from invapp.models import Collection, Project, Item, Bag, BagAction, Machine

now = datetime.datetime.utcnow().replace(tzinfo=utc)


class Command(BaseCommand):
    args = '<file path>'
    help = '''Import objects from a csv file.
All types can be imported, but to avoid bad references, import them in the
following order: Collections, Projects, Items, Bags.  The first value for
each line should be the item type. Below are the column orders for each type:

Collection, id, name, created (date), description, manager

Project, id, created (date), name, manager, collection (id), start_date,
end_date

Item, id, title, local_id, collection (id), project (id), created (date),
original_item_type, rawfiles_loc, qcfiles_loc, qafiles_loc, finfiles_loc,
ocrfiles_loc, notes

Bag, bagname, created, item, machine, path, bag_type

BagAction, bag (bagname), timestamp, action, note'''

    def handle(self, *args, **options):

        try:
            f = open(args[0], 'rb')
            payload_dir = os.path.join(os.path.dirname(args[0]), 'payloads')
            error_log = open('../logs/import_errors.log', 'a')
        except IndexError:
            raise CommandError('Please specify a csv file to read')
        reader = csv.reader(f)
        success = []
        errors = []
        rownum = 0
        for row in reader:
            rownum += 1
            object_type = row[0].lower()
            if object_type == 'collection':
                error = self._import_collection(row)
            elif object_type == 'project':
                error = self._import_project(row)
            elif object_type == 'item':
                error = self._import_item(row)
            elif object_type == 'bag':
                error = self._import_bag(row, payload_dir)
            elif object_type == 'bagaction':
                error = self._import_action(row)
            elif object_type == 'machine':
                error = self._import_machine(row)
            if error:
                msg = 'ERROR! at row %s: %s\n%s\n\n' % (rownum, error, ','.join(row))
                errors.append(msg)
                #print msg
            else:
                success.append(row)
                #print 'SUCCESS! %s' % ','.join(row)
        print '\nImport Complete\nTotal objects: %s' % str(len(success) +
            len(errors))
        print 'Successful: %s' % str(len(success))
        print 'Failed: %s' % str(len(errors))
        if errors:
            for error in errors:
                error_log.write(error)
        f.close()

    def _convert_date(self, date_string, null=False):
        try:
            format = '%Y-%m-%d %H:%M:%S'
            return make_aware(datetime.datetime.strptime(date_string, format),
                utc)
        except Exception:
            if null:
                return None
            return now

    def _import_collection(self, row):
        try:
            coll = Collection.objects.create(
                id=row[1],
                name=row[2],
                created=self._convert_date(row[3]),
                description=row[4],
                manager=row[5]
                )
            coll.save()
        except Exception, e:
            return e

    def _import_project(self, row):
        try:
            proj = Project.objects.create(
                id=row[1],
                created=self._convert_date(row[2]),
                name=row[3],
                manager=row[4],
                collection=Collection.objects.get(id=row[5]),
                start_date=self._convert_date(row[6], null=True),
                end_date=self._convert_date(row[7], null=True)
                )
            proj.save()
        except Exception, e:
            return e

    def _import_item(self, row):
        try:
            c = Collection.objects.filter(id=row[4])
            p = Project.objects.filter(id=row[5])
            collection = c[0] if c else None
            project = p[0] if p else None
            item = Item.objects.create(
                id=row[1],
                title=row[2],
                local_id=row[3],
                collection=collection,
                project=project,
                created=self._convert_date(row[6]),
                original_item_type=row[7],
                rawfiles_loc=row[8],
                qcfiles_loc=row[9],
                qafiles_loc=row[10],
                finfiles_loc=row[11],
                ocrfiles_loc=row[12],
                notes=row[13]
                )
            item.save()
        except Exception, e:
            return e

    def _import_bag(self, row, payload_dir):
        try:
            # handle preservation bags from bagdb that don't have id of item
            if row[3] == '' or row[3] == 'None':
                barcode = row[1][:14]
                item = Item.objects.get(local_id=barcode)
            else:
                item = Item.objects.get(id=row[3])
            bag_type = None
            for tup in settings.BAG_TYPES:
                if tup[1].lower() == row[6].lower():
                    bag_type = tup[0]
            bag_type = bag_type if bag_type else row[6]
            payload_file = open(os.path.join(payload_dir, row[1]))
            bag = Bag.objects.create(
                bagname=row[1],
                created=self._convert_date(row[2]),
                item=item,
                machine=Machine.objects.get(url=row[4]),
                path=row[5],
                bag_type=bag_type,
                payload_raw=payload_file.read()
                )
            bag.save()
        except Exception, e:
            return e

    def _import_action(self, row):
        try:
            action = BagAction.objects.create(
                bag=Bag.objects.get(bagname=row[1]),
                timestamp=self._convert_date(row[2]),
                action=row[3],
                note=row[4]
                )
            action.save()
        except Exception, e:
            return e

    def _import_machine(self, row):
        try:
            machine = Machine.objects.create(
                name = row[1],
                url = row[2]
                )
        except Exception, e:
            return e