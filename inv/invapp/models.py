from django.db import models


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
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)


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


class Bag(models.Model):
    bagnum = models.IntegerField()
    item = models.ForeignKey(Item, related_name='copy_item')
    machine = models.URLField()
    path = models.URLField()

    def fullpath(self):
        return '%s/%s' % (self.machine.rstrip('/'), self.path.lstrip('/'))

    def bagname(self):
        return '%s_bag%s' % (self.item.pid, self.bagnum)


class BagAction(models.Model):
    ACTIONS = (
        ('1', 'updated'),
        ('2', 'moved'),
        ('3', 'validated'),
        # and so on...
        )
    bag = models.ForeignKey(Bag, related_name='bag_action')
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=ACTIONS)
    note = models.TextField()
