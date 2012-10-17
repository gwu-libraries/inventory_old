import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc
from invapp.models import Collection, Project, Item, Bag, BagAction

now = datetime.datetime.utcnow().replace(tzinfo=utc)


class Command(BaseCommand):
	args = '<file path'
	help = '''Import objects from a csv file.
All types can be imported, but to avoid bad references, import them in the
following order: Collections, Projects, Items, Bags.  The first value for
each line should be the item type. Below are the column orders for each type:

Collection, pid, name, created (date), description, manager

Project, pid, created (date), name, manager, collection (pid), start_date, end_date

Item, pid, title, local_id, collection (pid), project (pid), created (date),
original_item_type, rawfiles_loc, qcfiles_loc, qafiles_loc, finfiles_loc,
ocrfiles_loc, notes

Bag, bagname, created, item, machine, path

BagAction, bag (bagname), timestamp, action, note'''

	def handle(self, *args, **options):

		try:
			f = open(args[0], 'rb')
		except IndexError:
			raise CommandError('Please specify a csv file to read')
		reader = csv.reader(f)
		success = []
		errors = []
		for row in reader:
			object_type = row[0].lower()
			if object_type == 'collection':
				error = self._import_collection(row)
			elif object_type == 'project':
				error = self._import_project(row)
			elif object_type == 'item':
				error = self._import_item(row)
			elif object_type == 'bag':
				error = self._import_bag(row)
			elif object_type == 'bagaction':
				error = self._import_action(row)
			if error:
				errors.append((row, error))
				print 'ERROR! %s' % ','.join(row)
			else:
				success.append(row)
				print 'SUCCESS! %s' % ','.join(row)
		print '\nImport Complete\nTotal objects: %s' % str(len(success)+len(errors))
		print 'Successful: %s' % str(len(success))
		print 'Failed: %s' % str(len(errors))
		if errors:
			print 'The following objects failed:'
			for error in errors:
				print error[0]
				print ','.join(error[1])
		f.close()


	def _convert_date(self, date_string, null=False):
		format = '%Y-%m-%d %H:%M:%S'
		try:
			return datetime.strptime(date_string, format)
		except Exception:
			if null:
				return None
			return now

	def _import_collection(self, row):
		try:
			coll = Collection.objects.create(
				pid = row[1],
				name = row[2],
				created = self._convert_date(row[3]),
				description = row[4],
				manager = row[5]
				)
			coll.save()
		except Exception, e:
			return e

	def _import_project(self, row):
		try:
			proj = Project.objects.create(
				pid = row[1],
				created = self._convert_date(row[2]),
				name = row[3],
				manager = row[4],
				collection = Collection.objects.get(pid=row[5]),
				start_date = self._convert_date(row[6], null=True),
				end_date = self._convert_date(row[7], null=True)
				)
			proj.save()
		except Exception, e:
			return e

	def _import_item(self, row):
		try:
			item = Item.objects.create(
				pid = row[1],
				title = row[2],
				local_id = row[3],
				collection = Collection.objects.get(pid=row[4]),
				project = Project.objects.get(pid=row[5]),
				created = self._convert_date(row[6]),
				original_item_type = row[7],
				rawfiles_loc = row[8],
				qcfiles_loc = row[9],
				qafiles_loc = row[10],
				finfiles_loc = row[11],
				ocrfiles_loc = row[12],
				notes = row[13]
				)
			item.save()
		except Exception, e:
			return e

	def _import_bag(self, row):
		try:
			bag = Bag.objects.create(
				bagname = row[1],
				created = self._convert_date(row[2]),
				item = Item.objects.get(pid=row[3]),
				machine = row[4],
				path = row[5]
				)
			bag.save()
		except Exception, e:
			return e

	def _import_action(self, row):
		try:
			action = BagAction.objects.create(
				bag = Bag.objects.get(bagname=row[1]),
				timestamp = self._convert_date(row[2]),
				action = row[3],
				note = row[4]
				)
			action.save()
		except Exception, e:
			return e