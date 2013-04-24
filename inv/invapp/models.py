import json

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from json_field import JSONField
from tastypie.models import create_api_key

from invapp.utils import merge_dicts


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
    stats = JSONField()

    def save(self, *args, **kwargs):
        if not self.stats:
            self.stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        super(Collection, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.items.count():
            return reduce(merge_dicts,
                map(lambda item: item.stats, self.items.all()))
        return {'total_count': 0, 'total_size': 0, 'types': {}}

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
            self.stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        super(Project, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.items.count():
            return reduce(merge_dicts,
                map(lambda item: item.stats, self.items.all()))
        return {'total_count': 0, 'total_size': 0, 'types': {}}



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
            self.stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        super(Item, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.bags.count():
            return reduce(merge_dicts,
                map(lambda bag: bag.stats, self.bags.all()))
        return {'total_count': 0, 'total_size': 0, 'types': {}}

    def purl(self):
        return '%s/%s' % (settings.ID_SERVICE_URL, self.id)


class Bag(models.Model):
    bagname = models.TextField(primary_key=True)
    created = models.DateTimeField()
    item = models.ForeignKey(Item, related_name='bags')
    machine = models.ForeignKey(Machine, related_name='bags')
    path = models.URLField()
    bag_type = models.CharField(max_length=1, choices=settings.BAG_TYPES)
    payload = models.TextField(blank=True)
    stats = JSONField()
    '''
    lines in payload should be formatted as such:
    relative_filepath_from_bag_directory file_size(MB)\n
    '''

    def urlpath(self):
        return '%s/%s' % (self.machine.url.rstrip('/'), self.path.lstrip('/'))

    def list_payload(self):
        return [line.split() for line in self.payload.split('\n') if line]

    def filecount(self):
        return self.stats['total_count']

    def size(self):
        return self.stats['total_size']

    def collect_stats(self):
        stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        if self.payload:
            for fpath, fsize in self.list_payload():
                ftype = fpath.split('.')[-1].lower() if '.' in fpath else 'unk'
                stats['total_count'] += 1
                stats['total_size'] += int(fsize)
                if ftype not in stats['types'].keys():
                    stats['types'][ftype] = {'count': 1, 'size': int(fsize)}
                else:
                    stats['types'][ftype]['count'] += 1
                    stats['types'][ftype]['size'] += int(fsize)
        return stats

    def save(self, *args, **kwargs):
        if not self.stats:
            self.stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        super(Bag, self).save(*args, **kwargs)


class BagAction(models.Model):
    bag = models.ForeignKey(Bag, related_name='bag_action')
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=settings.ACTIONS)
    note = models.TextField()

    class Meta:
        unique_together = ("bag", "action", "timestamp")
