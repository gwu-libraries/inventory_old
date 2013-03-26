from copy import deepcopy
from datetime import date, datetime
import json

from django.test import TestCase
from django.utils import timezone

from invapp.models import *

def now():
    return timezone.make_aware(datetime.now(), timezone.utc)

class ModelTestCase(TestCase):

    def test_payload(self):
        # set up hierarchy of fake objects for bag
        c1 = Collection(id='cccccccccccccccccc', name='test-collection-1',
            created=datetime.now())
        c1.save()
        p1 = Project(id='pppppppppppppppppp', name='test-project-1',
            manager='nobody', collection=c1, created=datetime.now())
        p1.save()
        i1 = Item(id='iiiiiiiiiiiiiiiiii', title='test-item-1', project=p1,
            created=datetime.now(), original_item_type='1')
        i1.save()
        m1 = Machine(name='test-machine-1', url='test-url-1')
        m1.save()

        # load bag with raw data
        bag = Bag(bagname='test-bag-1', created=datetime.now(), item=i1,
            machine=m1, path='test-path1', bag_type='1')
        self.assertEqual(bag.payload_stats, '')
        bag.save()
        result0 = json.loads(bag.payload_stats)
        self.assertEqual(result0['total_size'], 0)
        self.assertEqual(result0['total_count'], 0)
        self.assertEqual(len(result0['types'].keys()), 0)

        # now add payload data
        bag.payload_raw = """/data/METADATA/0123456789-dc.xml 2655
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
        result1 = bag.calc_pstats()
        self.assertEqual(expect['total_size'], result1['total_size'])
        self.assertEqual(expect['total_count'], result1['total_count'])
        for t in expect['types'].keys():
            self.assertEqual(expect['types'][t]['count'],
                result1['types'][t]['count'])
            self.assertEqual(expect['types'][t]['size'],
                result1['types'][t]['size'])

        # now save the bag and test the save() override
        bag.save()

        # test that data was saved correctly
        bag2 = Bag.objects.get(bagname='test-bag-1')
        result2 = json.loads(bag2.payload_stats)
        self.assertEqual(expect['total_size'], result2['total_size'])
        self.assertEqual(expect['total_count'], result2['total_count'])
        for t in expect['types'].keys():
            self.assertEqual(expect['types'][t]['count'],
                result2['types'][t]['count'])
            self.assertEqual(expect['types'][t]['size'],
                result2['types'][t]['size'])