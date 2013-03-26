import json

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from tastypie.models import create_api_key


models.signals.post_save.connect(create_api_key, sender=User)


class Machine(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)


class Collection(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    name = models.CharField(max_length=256)
    created = models.DateTimeField()
    description = models.TextField(blank=True)
    manager = models.CharField(max_length=256, blank=True)

    def purl(self):
        return '%s/%s' % (settings.ID_SERVICE_URL, self.id)


class Project(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    created = models.DateTimeField()
    name = models.CharField(max_length=256)
    manager = models.CharField(max_length=256)
    collection = models.ForeignKey(Collection,
        related_name='project_collection')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class Item(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    title = models.TextField(blank=True)
    local_id = models.CharField(max_length=256, blank=True)
    collection = models.ForeignKey(Collection, related_name='item_collection',
        null=True)
    project = models.ForeignKey(Project, related_name='item_project', null=True)
    created = models.DateTimeField()
    original_item_type = models.CharField(max_length=1, choices=settings.ITEM_TYPES)
    rawfiles_loc = models.URLField(blank=True)
    qcfiles_loc = models.URLField(blank=True)
    qafiles_loc = models.URLField(blank=True)
    finfiles_loc = models.URLField(blank=True)
    ocrfiles_loc = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def purl(self):
        return '%s/%s' % (settings.ID_SERVICE_URL, self.id)


class Bag(models.Model):
    bagname = models.TextField(primary_key=True)
    created = models.DateTimeField()
    item = models.ForeignKey(Item, related_name='bag_item')
    machine = models.ForeignKey(Machine, related_name='bag_machine')
    path = models.URLField()
    bag_type = models.CharField(max_length=1, choices=settings.BAG_TYPES)
    payload_raw = models.TextField(blank=True)
    payload_stats = models.TextField(blank=True)
    '''
    lines in payload should be formatted as such:
    relative_filepath_from_bag_directory file_size(MB)\n
    '''

    def urlpath(self):
        return '%s/%s' % (self.machine.url.rstrip('/'), self.path.lstrip('/'))

    def payload(self):
        return [line.split() for line in self.payload_raw.split('\n') if line]

    def pstats(self):
        return json.loads(self.payload_stats)

    def filecount(self):
        return self.pstats()['total_count']

    def size(self):
        return self.pstats()['total_size']

    def calc_pstats(self):
        json = {
            'total_count': 0,
            'total_size': 0,
            'types': {},
        }
        for f in self.payload():
            fpath, fsize = f[0], f[1]
            ftype = fpath.split('.')[-1].lower()
            json['total_count'] += 1
            json['total_size'] += int(fsize)
            if ftype not in json['types'].keys():
                json['types'][ftype] = {'count': 1, 'size': int(fsize)}
            else:
                json['types'][ftype]['count'] += 1
                json['types'][ftype]['size'] += int(fsize)
        return json

    def save(self, *args, **kwargs):
        self.payload_stats = json.dumps(self.calc_pstats())
        super(Bag, self).save(*args, **kwargs)


class BagAction(models.Model):
    bag = models.ForeignKey(Bag, related_name='bag_action')
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=settings.ACTIONS)
    note = models.TextField()

    class Meta:
        unique_together = ("bag", "action", "timestamp")