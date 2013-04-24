from datetime import datetime
import json

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from invapp.models import Machine, Collection, Project, Item, Bag
from invapp import utils

def now():
    return timezone.make_aware(datetime.now(), timezone.utc)


class ModelTestCase(TestCase):

    def test_payload(self):
        # set up hierarchy of fake objects for bag
        c1 = Collection(id='cccccccccccccccccc', name='test-collection-1',
            created=now())
        c1.save()
        p1 = Project(id='pppppppppppppppppp', name='test-project-1',
            manager='nobody', collection=c1, created=now())
        p1.save()
        i1 = Item(id='iiiiiiiiiiiiiiiiii', title='test-item-1', project=p1,
            created=now(), original_item_type='1')
        i1.save()
        m1 = Machine(name='test-machine-1', url='test-url-1')
        m1.save()

        # load bag with raw data
        bag = Bag(bagname='test-bag-1', created=now(), item=i1,
            machine=m1, path='test-path1', bag_type='1')
        bag.stats = bag.collect_stats()
        bag.save()
        self.assertEqual(bag.stats['total_size'], 0)
        self.assertEqual(bag.stats['total_count'], 0)
        self.assertEqual(len(bag.stats['types'].keys()), 0)

        # now add payload data
        bag.payload = """/data/METADATA/0123456789-dc.xml 2655
/data/METADATA/0123456789-MRC.xml 3256
/data/IMAGES/0123456789_pg1.jp2 1778740
/data/IMAGES/0123456789_pg2.jp2 1878756
/data/IMAGES/0123456789_pg3.jp2 1915879
/data/IMAGES/0123456789_pg1.tiff 1778740
/data/IMAGES/0123456789_pg2.tiff 1878756
/data/IMAGES/0123456789_pg3.tiff 1915879
"""
        # compare output of parsing method with expected result
        expect = {
            'total_count': 8,
            'total_size': 11152661,
            'types': {
                'xml': {'count': 2, 'size': 5911},
                'jp2': {'count': 3, 'size': 5573375},
                'tiff': {'count':3, 'size':5573375}
                }
            }
        bag.stats = bag.collect_stats()
        bag.save()
        self.assertEqual(expect['total_size'], bag.stats['total_size'])
        self.assertEqual(expect['total_count'], bag.stats['total_count'])
        for t in expect['types'].keys():
            self.assertEqual(expect['types'][t]['count'],
                bag.stats['types'][t]['count'])
            self.assertEqual(expect['types'][t]['size'],
                bag.stats['types'][t]['size'])


class AggregateStatsTestCase(TestCase):


    def setUp(self):
        c1 = Collection(id='cccccccccccccccccc', name='test-collection-1',
            created=now())
        c1.save()
        p1 = Project(id='pppppppppppppppppp', name='test-project-1',
            manager='nobody', collection=c1, created=now())
        p1.save()
        i1 = Item(id='iiiiiiiiiiiiiiiii1', title='test-item-1', project=p1,
            collection=c1, created=now(), original_item_type='1')
        i1.save()
        i2 = Item(id='iiiiiiiiiiiiiiiii2', title='test-item-2', project=p1,
            collection=c1, created=now(), original_item_type='1')
        i2.save()
        i3 = Item(id='iiiiiiiiiiiiiiiii3', title='test-item-3', project=p1,
            collection=c1, created=now(), original_item_type='1')
        i3.save()
        m1 = Machine(name='test-machine-1', url='test-url-1')
        m1.save()
        b1 = Bag(bagname='test-bag-1', created=now(), item=i1,
            machine=m1, path='test-path1', bag_type='1')
        b1.payload = """/data/METADATA/0123456789-dc.xml 11111
/data/METADATA/0123456789-MRC.xml 22222
/data/IMAGES/0123456789_pg1.jp2 3333333
/data/IMAGES/0123456789_pg2.jp2 4444444
/data/IMAGES/0123456789_pg3.jp2 5555555
/data/IMAGES/0123456789_pg1.tiff 666666
/data/IMAGES/0123456789_pg2.tiff 777777
/data/IMAGES/0123456789_pg3.tiff 888888
"""
        b1.stats = b1.collect_stats()
        b1.save()
        b2 = Bag(bagname='test-bag-2', created=now(), item=i1,
            machine=m1, path='test-path2', bag_type='1')
        b2.payload = """/data/METADATA/0123456789-dc.xml 12121
/data/METADATA/0123456789-MRC.xml 23232
/data/IMAGES/0123456789_pg1.jp2 3434343
/data/IMAGES/0123456789_pg2.jp2 4545454
/data/IMAGES/0123456789_pg3.jp2 5656565
/data/IMAGES/0123456789_pg1.tiff 676767
/data/IMAGES/0123456789_pg2.tiff 787878
/data/IMAGES/0123456789_pg3.tiff 898989
"""
        b2.stats = b2.collect_stats()
        b2.save()


        b3 = Bag(bagname='test-bag-3', created=now(), item=i2,
            machine=m1, path='test-path3', bag_type='1')
        b3.payload = """/data/METADATA/0123456789-dc.xml 12121
/data/METADATA/0123456789-MRC.xml 23232
/data/IMAGES/0123456789_pg1.jp2 3434343
/data/IMAGES/0123456789_pg2.jp2 4545454
/data/IMAGES/0123456789_pg3.jp2 5656565
/data/IMAGES/0123456789_pg1.tiff 676767
/data/IMAGES/0123456789_pg2.tiff 787878
/data/IMAGES/0123456789_pg3.tiff 898989
"""
        b3.stats = b3.collect_stats()
        b3.save()
        b4 = Bag(bagname='test-bag-4', created=now(), item=i2,
            machine=m1, path='test-path4', bag_type='1')
        b4.payload = """/data/METADATA/0123456789-dc.xml 12345
/data/METADATA/0123456789-MRC.xml 34578
/data/IMAGES/0123456789_pg1.jp2 987654
/data/IMAGES/0123456789_pg2.jp2 3214567
/data/IMAGES/0123456789_pg3.jp2 654789
/data/IMAGES/0123456789_pg1.tiff 489751
/data/IMAGES/0123456789_pg2.tiff 584321
/data/IMAGES/0123456789_pg3.tiff 782345
"""
        b4.stats = b4.collect_stats()
        b4.save()


        b5 = Bag(bagname='test-bag-5', created=now(), item=i3,
            machine=m1, path='test-path5', bag_type='1')
        b5.payload = """/data/METADATA/0123456789-dc.xml 12121
/data/METADATA/0123456789-MRC.xml 23232
/data/IMAGES/0123456789_pg1.tiff 676767
/data/IMAGES/0123456789_pg2.tiff 787878
/data/IMAGES/0123456789_pg3.tiff 898989
"""
        b5.stats = b5.collect_stats()
        b5.save()
        b6 = Bag(bagname='test-bag-6', created=now(), item=i3,
            machine=m1, path='test-path6', bag_type='1')
        b6.payload = """/data/METADATA/0123456789-dc.xml 38479
/data/METADATA/0123456789-MRC.xml 62134
/data/IMAGES/0123456789_pg1.jp2 6489723
/data/IMAGES/0123456789_pg2.jp2 8984567
/data/IMAGES/0123456789_pg3.jp2 1568974
"""
        b6.stats = b6.collect_stats()
        b6.save()

        self.empty_stats = {'total_count': 0, 'total_size': 0, 'types': {}}

        self.expected = {
            'items': {
                'i1': {
                    'total_count': 16,
                    'total_size': 31735345,
                    'types': {
                        'xml': {'count': 4, 'size': 68686},
                        'jp2': {'count': 6, 'size': 26969694}, 
                        'tiff': {'count': 6, 'size': 4696965}
                    }
                },
                'i2': {
                    'total_count': 16,
                    'total_size': 22795699,
                    'types': {
                        'xml': {'count': 4, 'size': 82276},
                        'jp2': {'count': 6, 'size': 18493372}, 
                        'tiff': {'count': 6, 'size': 4220051}
                    }
                },
                'i3': {
                    'total_count': 10,
                    'total_size': 19542864,
                    'types': {
                        'xml': {'count': 4, 'size': 135966},
                        'jp2': {'count': 3, 'size': 17043264}, 
                        'tiff': {'count': 3, 'size': 2363634}
                    }
                }
            },
            'projects': {
                'p1': {
                    'total_count': 42,
                    'total_size': 74073908,
                    'types': {
                        'xml': {'count': 12, 'size': 286928},
                        'jp2': {'count': 15, 'size': 62506330}, 
                        'tiff': {'count': 15, 'size': 11280650}
                    }
                }
            },
            'collections': {
                'c1': {
                    'total_count': 42,
                    'total_size': 74073908,
                    'types': {
                        'xml': {'count': 12, 'size': 286928},
                        'jp2': {'count': 15, 'size': 62506330}, 
                        'tiff': {'count': 15, 'size': 11280650}
                    }
                }
            }
        }


    def test_collect_stats_functions(self):
        i1 = Item.objects.get(id='iiiiiiiiiiiiiiiii1')
        self.assertTrue(utils.compare_dicts(i1.stats, self.empty_stats))
        i1.stats = i1.collect_stats()
        i1.save()
        self.assertTrue(utils.compare_dicts(i1.stats,
            self.expected['items']['i1']))

        i2 = Item.objects.get(id='iiiiiiiiiiiiiiiii2')
        self.assertTrue(utils.compare_dicts(i2.stats, self.empty_stats))
        i2.stats = i2.collect_stats()
        i2.save()
        self.assertTrue(utils.compare_dicts(i2.stats,
            self.expected['items']['i2']))

        i3 = Item.objects.get(id='iiiiiiiiiiiiiiiii3')
        self.assertTrue(utils.compare_dicts(i3.stats, self.empty_stats))
        i3.stats = i3.collect_stats()
        i3.save()
        self.assertTrue(utils.compare_dicts(i3.stats,
            self.expected['items']['i3']))

        p1 = Project.objects.get(id='pppppppppppppppppp')
        p1.stats = p1.collect_stats()
        p1.save()
        self.assertTrue(utils.compare_dicts(p1.stats,
            self.expected['projects']['p1']))

        c1 = Collection.objects.get(id='cccccccccccccccccc')
        c1.stats = c1.collect_stats()
        c1.save()
        self.assertTrue(utils.compare_dicts(c1.stats,
            self.expected['collections']['c1']))

    def test_update_object_stats(self):
        # test by passing object directly
        i1 = Item.objects.get(id='iiiiiiiiiiiiiiiii1')
        self.assertTrue(utils.compare_dicts(i1.stats, self.empty_stats))
        utils.update_object_stats(i1)
        self.assertTrue(utils.compare_dicts(i1.stats,
            self.expected['items']['i1']))

        # test by passing model and id
        utils.update_object_stats(model=Item, id='iiiiiiiiiiiiiiiii2')
        i2 = Item.objects.get(id='iiiiiiiiiiiiiiiii2')
        self.assertTrue(utils.compare_dicts(i2.stats,
            self.expected['items']['i2']))

    def test_update_model_stats(self):
        errors = utils.update_model_stats(Item)
        self.assertEqual(errors, [])
        self.assertTrue(not errors)

        i1 = Item.objects.get(id='iiiiiiiiiiiiiiiii1')
        self.assertTrue(utils.compare_dicts(i1.stats,
            self.expected['items']['i1']))

        i2 = Item.objects.get(id='iiiiiiiiiiiiiiiii2')
        self.assertTrue(utils.compare_dicts(i2.stats,
            self.expected['items']['i2']))

        i3 = Item.objects.get(id='iiiiiiiiiiiiiiiii3')
        self.assertTrue(utils.compare_dicts(i3.stats,
            self.expected['items']['i3']))

    def test_update_all_stats(self):
        errors = utils.update_all_stats()
        self.assertEqual(errors, [])
        self.assertTrue(not errors)

        i1 = Item.objects.get(id='iiiiiiiiiiiiiiiii1')
        self.assertTrue(utils.compare_dicts(i1.stats,
            self.expected['items']['i1']))

        i2 = Item.objects.get(id='iiiiiiiiiiiiiiiii2')
        self.assertTrue(utils.compare_dicts(i2.stats,
            self.expected['items']['i2']))

        i3 = Item.objects.get(id='iiiiiiiiiiiiiiiii3')
        self.assertTrue(utils.compare_dicts(i3.stats,
            self.expected['items']['i3']))

        p1 = Project.objects.get(id='pppppppppppppppppp')
        self.assertTrue(utils.compare_dicts(p1.stats,
            self.expected['projects']['p1']))

        c1 = Collection.objects.get(id='cccccccccccccccccc')
        self.assertTrue(utils.compare_dicts(c1.stats,
            self.expected['collections']['c1']))

    def test_stats_on_empty_objects(self):
        expected = self.empty_stats
        c1 = Collection(id='nobagscollection', name='test-collection-2',
            created=now())
        c1.save()
        self.assertTrue(utils.compare_dicts(c1.stats, expected))
        p1 = Project(id='nobagsproject', name='test-project-2',
            manager='nobody', collection=c1, created=now())
        p1.save()
        self.assertTrue(utils.compare_dicts(p1.stats, expected))
        i1 = Item(id='nobagsitem', title='test-item-1', project=p1,
            collection=c1, created=now(), original_item_type='1')
        i1.stats = i1.collect_stats()
        i1.save()
        p1.stats = p1.collect_stats()
        c1.stats = c1.collect_stats()
        self.assertTrue(utils.compare_dicts(i1.stats, expected))
        self.assertTrue(utils.compare_dicts(p1.stats, expected))
        self.assertTrue(utils.compare_dicts(c1.stats, expected))
    
    def test_mgmt_cmd_all(self):
        call_command('update_stats', All=True)

        i1 = Item.objects.get(id='iiiiiiiiiiiiiiiii1')
        self.assertTrue(utils.compare_dicts(i1.stats,
            self.expected['items']['i1']))

        i2 = Item.objects.get(id='iiiiiiiiiiiiiiiii2')
        self.assertTrue(utils.compare_dicts(i2.stats,
            self.expected['items']['i2']))

        i3 = Item.objects.get(id='iiiiiiiiiiiiiiiii3')
        self.assertTrue(utils.compare_dicts(i3.stats,
            self.expected['items']['i3']))

        p1 = Project.objects.get(id='pppppppppppppppppp')
        self.assertTrue(utils.compare_dicts(p1.stats,
            self.expected['projects']['p1']))

        c1 = Collection.objects.get(id='cccccccccccccccccc')
        self.assertTrue(utils.compare_dicts(c1.stats,
            self.expected['collections']['c1']))
    
    def test_mgmt_cmd_single_item(self):
        call_command('update_stats', item='iiiiiiiiiiiiiiiii1')

        i1 = Item.objects.get(id='iiiiiiiiiiiiiiiii1')
        self.assertTrue(utils.compare_dicts(i1.stats,
            self.expected['items']['i1']))
    
    def test_mgmt_cmd_many_item_single_proj_single_coll(self):
        call_command('update_stats', Items=True)
        call_command('update_stats', project='pppppppppppppppppp')
        call_command('update_stats', collection='cccccccccccccccccc')

        i1 = Item.objects.get(id='iiiiiiiiiiiiiiiii1')
        self.assertTrue(utils.compare_dicts(i1.stats,
            self.expected['items']['i1']))

        i2 = Item.objects.get(id='iiiiiiiiiiiiiiiii2')
        self.assertTrue(utils.compare_dicts(i2.stats,
            self.expected['items']['i2']))

        i3 = Item.objects.get(id='iiiiiiiiiiiiiiiii3')
        self.assertTrue(utils.compare_dicts(i3.stats,
            self.expected['items']['i3']))

        p1 = Project.objects.get(id='pppppppppppppppppp')
        self.assertTrue(utils.compare_dicts(p1.stats,
            self.expected['projects']['p1']))

        c1 = Collection.objects.get(id='cccccccccccccccccc')
        self.assertTrue(utils.compare_dicts(c1.stats,
            self.expected['collections']['c1']))

    def test_mgmt_cmd_many_models(self):
        call_command('update_stats', Items=True)
        call_command('update_stats', Projects=True)
        call_command('update_stats', Collections=True)

        i1 = Item.objects.get(id='iiiiiiiiiiiiiiiii1')
        self.assertTrue(utils.compare_dicts(i1.stats,
            self.expected['items']['i1']))

        i2 = Item.objects.get(id='iiiiiiiiiiiiiiiii2')
        self.assertTrue(utils.compare_dicts(i2.stats,
            self.expected['items']['i2']))

        i3 = Item.objects.get(id='iiiiiiiiiiiiiiiii3')
        self.assertTrue(utils.compare_dicts(i3.stats,
            self.expected['items']['i3']))

        p1 = Project.objects.get(id='pppppppppppppppppp')
        self.assertTrue(utils.compare_dicts(p1.stats,
            self.expected['projects']['p1']))

        c1 = Collection.objects.get(id='cccccccccccccccccc')
        self.assertTrue(utils.compare_dicts(c1.stats,
            self.expected['collections']['c1']))
