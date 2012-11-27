from django.db import models
from django.conf import settings


class Machine(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)


class Collection(models.Model):
    pid = models.CharField(max_length=18, unique=True)
    name = models.CharField(max_length=256)
    created = models.DateTimeField()
    description = models.TextField(blank=True)
    manager = models.CharField(max_length=256, blank=True)


class Project(models.Model):
    pid = models.CharField(max_length=18, unique=True)
    created = models.DateTimeField()
    name = models.CharField(max_length=256)
    manager = models.CharField(max_length=256)
    collection = models.ForeignKey(Collection,
        related_name='project_collection')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class Item(models.Model):
    TYPES = (
        ('1', 'book'),
        ('2', 'microfilm'),
        )
    pid = models.CharField(max_length=18, unique=True)
    title = models.CharField(max_length=256)
    local_id = models.CharField(max_length=256, blank=True)
    collection = models.ForeignKey(Collection, related_name='item_collection')
    project = models.ForeignKey(Project, related_name='item_project')
    created = models.DateTimeField()
    original_item_type = models.CharField(max_length=1, choices=TYPES)
    rawfiles_loc = models.URLField(blank=True)
    qcfiles_loc = models.URLField(blank=True)
    qafiles_loc = models.URLField(blank=True)
    finfiles_loc = models.URLField(blank=True)
    ocrfiles_loc = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def pidurl(self):
        return '%s/%s' % (settings.ID_SERVICE_URL, self.pid)


class Bag(models.Model):
    BAG_TYPES = (
        ('1', 'Access'),
        ('2', 'Preservation'),
        ('3', 'Export')
        )
    bagname = models.CharField(max_length=36, unique=True)
    created = models.DateTimeField()
    item = models.ForeignKey(Item, related_name='bag_item')
    machine = models.ForeignKey(Machine, related_name='bag_machine')
    path = models.URLField()
    bag_type = models.CharField(max_length=1, choices=BAG_TYPES)
    payload = models.TextField(blank=True)
    '''
    lines in payload should be formatted as such:
    relative_filepath_from_bag_directory file_size(MB)\n
    '''

    def urlpath(self):
        return '%s/%s' % (self.machine.url.rstrip('/'), self.path.lstrip('/'))

    def listpayload(self):
        return [line.split() for line in self.payload.split('\n')]

    def parse_payload(self):
        payloaddict = {
            'files': [],
            'total_files': 0,
            'total_size': 0,
            'total_file_types': {},
            'total_size_types': {}
        }
        if self.payload:
            for line in self.payload.split('\n'):
                filepath, filesize = line.split()
                filetype = filepath[-3:]
                payloaddict['files'].append((filepath, filesize))
                payloaddict['total_files'] += 1
                payloaddict['total_size'] += int(filesize)
                if filetype not in payloaddict['total_file_types'].keys():
                    payloaddict['total_file_types'][filetype] = 1
                    payloaddict['total_size_types'][filetype] = int(filesize)
                else:
                    payloaddict['total_file_types'][filetype] += 1
                    payloaddict['total_size_types'][filetype] += int(filesize)
        self.payloaddict = payloaddict
        return self.payloaddict


class BagAction(models.Model):
    ACTIONS = (
        ('1', 'updated'),
        ('2', 'moved'),
        ('3', 'validated'),
        ('4', 'imported to DSpace')
        # and so on...
        )
    bag = models.ForeignKey(Bag, related_name='bag_action')
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=ACTIONS)
    note = models.TextField()