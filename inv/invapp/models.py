import json

from json_field import JSONField
from tastypie.models import create_api_key

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.timezone import now

from invapp.idservice import mintandbind
from invapp.utils import merge_dicts


models.signals.post_save.connect(create_api_key, sender=User)


class Machine(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(null=True, blank=True, default=None, unique=True)
    ip = models.IPAddressField(null=True, blank=True, default=None,
                               unique=True)
    notes = models.TextField(blank=True)
    access_root = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.ip == '':
            self.ip = None
        if self.url == '':
            self.url = None
        super(Machine, self).save(*args, **kwargs)


class Collection(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    name = models.CharField(max_length=256)
    created = models.DateTimeField(default=now)
    description = models.TextField(blank=True)
    manager = models.CharField(max_length=256, blank=True)
    access_loc = models.URLField(blank=True)
    stats = JSONField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = mintandbind(objtype='c', objurl=self.access_loc,
                                  description=self.name)
        if not self.stats:
            self.stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        super(Collection, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.items.count():
            return reduce(merge_dicts,
                          map(lambda item: item.stats, self.items.all()))
        return {'total_count': 0, 'total_size': 0, 'types': {}}

    def __unicode__(self):
        return self.name


class Project(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    created = models.DateTimeField(default=now)
    name = models.CharField(max_length=256)
    collection = models.ForeignKey(Collection, related_name='projects',
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL)
    stats = JSONField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = mintandbind(objtype='p', description=self.name)
        if not self.stats:
            self.stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        super(Project, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.items.count():
            return reduce(merge_dicts,
                          map(lambda item: item.stats, self.items.all()))
        return {'total_count': 0, 'total_size': 0, 'types': {}}

    def __unicode__(self):
        return self.name


class Item(models.Model):
    id = models.CharField(max_length=settings.ID_MAX_LENGTH, primary_key=True)
    title = models.TextField(blank=True)
    local_id = models.CharField(max_length=256, blank=True)
    collection = models.ForeignKey(Collection, related_name='items',
                                   null=True, default=None, blank=True,
                                   on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, related_name='items', null=True,
                                blank=True, default=None,
                                on_delete=models.SET_NULL)
    created = models.DateTimeField(default=now)
    original_item_type = models.CharField(max_length=1,
                                          choices=settings.ITEM_TYPES)
    notes = models.TextField(blank=True)
    access_loc = models.URLField(blank=True)
    stats = JSONField()

    def save(self, *args, **kwargs):
        if not self.id:
            desc = 'local_id: %s; title: %s;' % (self.local_id, self.title)
            self.id = mintandbind(objtype='i', objurl=self.access_loc,
                                  description=desc)
        if not self.stats:
            self.stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        super(Item, self).save(*args, **kwargs)

    def collect_stats(self):
        if self.bags.count():
            return reduce(merge_dicts,
                          map(lambda bag: bag.stats, self.bags.all()))
        return {'total_count': 0, 'total_size': 0, 'types': {}}

    def __unicode__(self):
        return self.title


class Bag(models.Model):
    bagname = models.TextField(primary_key=True)
    created = models.DateTimeField(default=now)
    item = models.ForeignKey(Item, related_name='bags',
                             on_delete=models.PROTECT)
    machine = models.ForeignKey(Machine, related_name='bags',
                                on_delete=models.PROTECT)
    path = models.CharField(max_length=255)
    bag_type = models.CharField(max_length=1, choices=settings.BAG_TYPES)
    payload = models.TextField(blank=True)
    stats = JSONField()
    '''
    lines in payload should be formatted as such:
    relative_filepath_from_bag_directory file_size(MB)\n
    '''

    def access_url(self):
        url = self.machine.url if self.machine.url else self.machine.ip
        if not url:
            return None
        # FIXME: really?  what about https?
        if not url.startswith('http://'):
            url = 'http://%s' % url
        mach_path_parts = self.machine.access_root.strip('/').split('/')
        path_parts = self.path.strip('/').split('/')
        for i, value in enumerate(path_parts):
            if i == len(mach_path_parts) or value != mach_path_parts[i]:
                return '/'.join([url] + path_parts[i:])

    def list_payload(self):
        return [line.split() for line in self.payload.split('\n') if line]

    def list_payload_str(self):
        return json.dumps(self.list_payload())

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
        if not self.bagname:
            # derive bagname from item ID and bag type,
            # but with no forward slashes (creates problems on file system)
            itemid = self.item.id.replace('/', '_')
            bagtype = self.get_bag_type_display().upper()
            bagname = '%s_%s_BAG' % (itemid, bagtype)
            # differentiate between multiple copies using simple incrementer
            other_copies = self.item.bags.filter(bagname__startswith=bagname)
            if len(other_copies) > 0:
                nums = [int(o.bagname.split('_')[-1]) for o in other_copies]
                copy_num = sorted(nums)[-1] + 1
            else:
                copy_num = 1
            self.bagname = '%s_%s' % (bagname, copy_num)
        if not self.stats:
            self.stats = {'total_count': 0, 'total_size': 0, 'types': {}}
        super(Bag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.bagname


class BagAction(models.Model):
    bag = models.ForeignKey(Bag, related_name='bag_action')
    timestamp = models.DateTimeField(default=now)
    action = models.CharField(max_length=1, choices=settings.ACTIONS)
    note = models.TextField()

    class Meta:
        unique_together = ("bag", "action", "timestamp")

    def __unicode__(self):
        return '%s : %s' % (self.bag.bagname, self.action)
