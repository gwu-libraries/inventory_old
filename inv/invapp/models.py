from django.db import models


class Collection(models.Model):
    collection_id = models.CharField(max_length=16)
    name = models.CharField(max_length=256)
    created = models.DateTimeField()
    description = models.TextField(blank=True)
    manager = models.CharField(max_length=256, blank=True)


class Project(models.Model):
    create_date = models.DateTimeField()
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
    item_id = models.CharField(max_length=16)
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
    item = models.ForeignKey(Item, related_name='copy_item')
    machine = models.URLField()
    path = models.URLField()

    def get_full_path(self):
        pass


class BagAction(models.Model):
    ACTIONS = (
        ('1', 'updated'),
        ('2', 'validated'),
        # and so on...
        )
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=ACTIONS)
    note = models.TextField()
