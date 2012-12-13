from datetime import date, datetime

from django.test import TestCase
from django.utils import timezone

from invapp.models import *

def now():
    return timezone.make_aware(datetime.now(), timezone.utc)

class ModelTestCase(TestCase):

    def test_parse_payload(self):
        pass