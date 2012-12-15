from copy import deepcopy
from datetime import date, datetime

from django.test import TestCase
from django.utils import timezone

from invapp.models import *

def now():
    return timezone.make_aware(datetime.now(), timezone.utc)

class ModelTestCase(TestCase):

    def test_payload(self):
        self.maxDiff = None
        # load bag with raw data
        bag = Bag()
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
        pdict = {
            'size': 11152661,
            'files': [
                ('/data/METADATA/0123456789-dc.xml', '2655'),
                ('/data/METADATA/0123456789-MRC.xml', '3256'),
                ('/data/IMAGES/0123456789_pg1.jp2', '1778740'),
                ('/data/IMAGES/0123456789_pg2.jp2', '1878756'),
                ('/data/IMAGES/0123456789_pg3.jp2', '1915879'),
                ('/data/IMAGES/0123456789_pg1.tiff', '1778740'),
                ('/data/IMAGES/0123456789_pg2.tiff', '1878756'),
                ('/data/IMAGES/0123456789_pg3.tiff', '1915879')],
            'types': {
                'xml': [2, 5911],
                'jp2': [3, 5573375],
                'tiff': [3, 5573375]}}
        self.assertEqual(pdict['size'], bag.payload['size'])
        for f in pdict['files']:
            self.assertTrue(f in bag.payload['files'])
        for t in pdict['types'].keys():
            self.assertEqual(pdict['types'][t][0], bag.payload['types'][t][0])
            self.assertEqual(pdict['types'][t][1], bag.payload['types'][t][1])
        
        # test ability to wipe out parsed data
        del bag.payload
        self.assertRaises(AttributeError, getattr, bag, 'payload_parsed')
        self.assertTrue(bag.payload)
        
        # test ability to overwrite
        bag.parse_payload()
        pdict2 = deepcopy(pdict)
        pdict2['files'].append(('/data/PDF/0123456789.pdf', 454561))
        pdict2['size'] += 454561
        pdict2['types']['pdf'] = [1, 454561]
        bag.payload = pdict2
        self.assertEqual(pdict2['size'], bag.payload['size'])
        for f in pdict2['files']:
            self.assertTrue(f in bag.payload['files'])
        for t in pdict2['types'].keys():
            self.assertEqual(pdict2['types'][t][0], bag.payload['types'][t][0])
            self.assertEqual(pdict2['types'][t][1], bag.payload['types'][t][1])