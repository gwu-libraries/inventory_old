import json

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from json_field import JSONField
from tastypie.models import create_api_key

from invapp.utils import merge_dicts


models.signals.post_save.connect(create_api_key, sender=User)


empty_stats = {'total_count': 0, 'total_size': 0, 'types': {}}


class Machine(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)


class Collection(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    name = models.CharField(max_length=256)
    created = models.DateTimeField()
    description = models.TextField(blank=True)
    manager = models.CharField(max_length=256, blank=True)
    stats = JSONField()

    def save(self, *args, **kwargs):
        if not self.stats:
            self.stats = empty_stats
        super(Collection, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.items.count():
            return reduce(merge_dicts,
                map(lambda item: item.stats, self.items.all()))
        return empty_stats

    def purl(self):
        return '%s/%s' % (settings.ID_SERVICE_URL, self.id)


class Project(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    created = models.DateTimeField()
    name = models.CharField(max_length=256)
    manager = models.CharField(max_length=256)
    collection = models.ForeignKey(Collection, related_name='projects')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    stats = JSONField()

    def save(self, *args, **kwargs):
        if not self.stats:
            self.stats = empty_stats
        super(Project, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.items.count():
            return reduce(merge_dicts,
                map(lambda item: item.stats, self.items.all()))
        return empty_stats



class Item(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    title = models.TextField(blank=True)
    local_id = models.CharField(max_length=256, blank=True)
    collection = models.ForeignKey(Collection, related_name='items',
        null=True)
    project = models.ForeignKey(Project, related_name='items', null=True)
    created = models.DateTimeField()
    original_item_type = models.CharField(max_length=1,
        choices=settings.ITEM_TYPES)
    rawfiles_loc = models.URLField(blank=True)
    qcfiles_loc = models.URLField(blank=True)
    qafiles_loc = models.URLField(blank=True)
    finfiles_loc = models.URLField(blank=True)
    ocrfiles_loc = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    stats = JSONField()

    def save(self, *args, **kwargs):
        if not self.stats:
            self.stats = empty_stats
        super(Item, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.bags.count():
            return reduce(merge_dicts,
                map(lambda bag: bag.pstats(), self.bags.all()))
        return empty_stats

    def purl(self):
        return '%s/%s' % (settings.ID_SERVICE_URL, self.id)


class Bag(models.Model):
    bagname = models.TextField(primary_key=True)
    created = models.DateTimeField()
    item = models.ForeignKey(Item, related_name='bags')
    machine = models.ForeignKey(Machine, related_name='bags')
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
