from django.db import models
from django.conf import settings


class Machine(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)


class Collection(models.Model):
    pid = models.CharField(max_length=settings.ID_MAX_LENGTH, unique=True)
    name = models.CharField(max_length=256)
    created = models.DateTimeField()
    description = models.TextField(blank=True)
    manager = models.CharField(max_length=256, blank=True)


class Project(models.Model):
    pid = models.CharField(max_length=settings.ID_MAX_LENGTH, unique=True)
    created = models.DateTimeField()
    name = models.CharField(max_length=256)
    manager = models.CharField(max_length=256)
    collection = models.ForeignKey(Collection,
        related_name='project_collection')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class Item(models.Model):
    pid = models.CharField(max_length=settings.ID_MAX_LENGTH, unique=True)
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
        return '%s/%s' % (settings.ID_SERVICE_URL, self.pid)


class Bag(models.Model):
    bagname = models.TextField(unique=True)
    created = models.DateTimeField()
    item = models.ForeignKey(Item, related_name='bag_item')
    machine = models.ForeignKey(Machine, related_name='bag_machine')
    path = models.URLField()
    bag_type = models.CharField(max_length=1, choices=settings.BAG_TYPES)
    payload_raw = models.TextField(blank=True)
    '''
    lines in payload should be formatted as such:
    relative_filepath_from_bag_directory file_size(MB)\n
    '''

    def urlpath(self):
        return '%s/%s' % (self.machine.url.rstrip('/'), self.path.lstrip('/'))

    @property
    def payload(self):
        # create a data dict if one doesn't exist and use that
        # to avoid recalculating data every time the property is needed
        try:
            return self.payload_parsed
        except AttributeError:
            return self.parse_payload()

    @payload.setter
    def payload(self, data):
        assert isinstance(data, dict), 'payload must be a dictionary'
        assert isinstance(data['files'], list), \
            'payload must contain a list of file data'
        assert all(isinstance(f, tuple) for f in data['files']), \
            'files must contain tuples of format (filepath, filesize)'
        assert isinstance(data['size'], int), \
            'payload must contain aggregate size information'
        assert isinstance(data['types'], dict), \
            'payload must have a subdictionary "types"'
        assert all(isinstance(data['types'][d],
            list) for d in data['types'].keys()), \
            'payload["types"] must be a dict with lists [count, size]'
        self.payload_parsed = data

    @payload.deleter
    def payload(self):
        self.__dict__.pop('payload_parsed')

    def parse_payload(self):
        payload_parsed = {
            'files': [],
            'size': 0,
            'types': {},
        }
        for line in self.payload_raw.split('\n'):
            if line:
                filepath, filesize = line.split()
                filetype = filepath.split('.')[-1]
                payload_parsed['files'].append((filepath, filesize))
                payload_parsed['size'] += int(filesize)
                if filetype not in payload_parsed['types'].keys():
                    payload_parsed['types'][filetype] = [1, int(filesize)]
                else:
                    payload_parsed['types'][filetype][0] += 1
                    payload_parsed['types'][filetype][1] += int(filesize)
        payload_parsed['files'] = sorted(payload_parsed['files'],
            key=lambda filetup: filetup[0])
        self.payload_parsed = payload_parsed
        return self.payload_parsed


class BagAction(models.Model):
    bag = models.ForeignKey(Bag, related_name='bag_action')
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=settings.ACTIONS)
    note = models.TextField()

    class Meta:
        unique_together = ("bag", "action", "timestamp")