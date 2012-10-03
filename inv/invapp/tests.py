from datetime import date, datetime

from django.test import TestCase
from django.utils import timezone

from invapp.models import Collection, Project, Item, Bag, BagAction

def now():
    return timezone.make_aware(datetime.now(), timezone.utc)

class ModelTestCase(TestCase):

    def test_object_creation(self):
        #insert a test collection
        c1 = Collection(pid='38989/c01eeddeeddk', name='IMLS',
            created=now(), manager='Joshua Gomez',
            description='A test collection that we will throw away')
        c1.save()
        #test collection retrieval
        c2 = Collection.objects.get(pid=c1.pid)
        self.assertEqual(c2.name, c1.name)
        self.assertEqual(c2.created, c1.created)
        self.assertEqual(c2.description, c1.description)
        self.assertEqual(c2.manager, c1.manager)
        #insert a test project
        p1 = Project(created=now(), name='Book Scanning Project',
            manager='Rosy Metz', start_date=date(2012, 9, 1),
            end_date=date(2012, 12, 1), collection=c2)
        p1.save()
        #test project retrieval
        p2 = Project.objects.get(name=p1.name)
        self.assertEqual(p2.name, p1.name)
        self.assertEqual(p2.created, p1.created)
        self.assertEqual(p2.manager, p1.manager)
        self.assertEqual(p2.start_date, p1.start_date)
        self.assertEqual(p2.end_date, p1.end_date)
        self.assertEqual(p2.collection, c2)
        #insert test items
        i1 = Item(pid='38989/c01012345678', title="Pudd'n'head Wilson",
            local_id='2619023338272', collection=c2, project=p2, created=now(),
            original_item_type='1')
        i1.save()
        c3 = Collection(pid='38989/c01aabbccddk', name='IBT',
            created=now(), manager='Joshua Gomez',
            description='A test collection that we will throw away')
        c3.save()
        p3 = Project(created=now(), name='Microfilm Scanning Project',
            manager='Rosy Metz', start_date=date(2012, 9, 1),
            end_date=date(2013, 10, 1), collection=c2)
        p3.save()
        i2 = Item(pid='38989/c01987654321', title='Al Capone',
            local_id='lac0004_r87_sg77', collection=c3, project=p3,
            created=now(), original_item_type='2')
        i2.save()
        #test item retrieval
        for i in (i1, i2):
            ti = Item.objects.get(pid=i.pid)
            self.assertEqual(ti.title, i.title)
            self.assertEqual(ti.local_id, i.local_id)
            self.assertEqual(ti.collection, i.collection)
            self.assertEqual(ti.project, i.project)
            self.assertEqual(ti.created, i.created)
            self.assertEqual(ti.original_item_type, i.original_item_type)
        #insert test bags
        b1 = Bag(item=i1, bagnum=1, machine='gwdspace.wrlc.org', 
            path='/dspace1/IMLS/261902338272')
        b1.save()
        b2 = Bag(item=i2, bagnum=1, machine='gwdspace.wrlc.org',
            path='/dspace2/IBT-microfilm/lac0004_r87_sg77')
        b2.save()
        #test bag retrieval
        b3 = Bag.objects.get(item=i1, bagnum=1)
        self.assertEqual(b3.item, b1.item)
        self.assertEqual(b3.bagname(), '38989/c01012345678_bag1')
        self.assertEqual(b3.fullpath(),
            'gwdspace.wrlc.org/dspace1/IMLS/261902338272')
        b4 = Bag.objects.get(item=i2, bagnum=1)
        self.assertEqual(b2, b4)
        #insert bag actions
        ba1 = BagAction(bag=b1, timestamp=now(), action='1',
            note='file x added to bag')
        ba1.save()
        ba2 = BagAction(bag=b1, timestamp=now(), action='2',
            note='bag moved to dspace server')
        ba2.save()
        ba3 = BagAction(bag=b1, timestamp=now(), action='3',
            note='bag validated')
        ba3.save()
        #test bagaction retrieval
        actions = BagActions.objects.filter(bag=b1)
        self.assertEqual(len(actions), 3)
