from tastypie.resources import ModelResource
from invapp.models import *


class CollectionResource(ModelResource):
    class Meta:
        queryset = Collection.objects.all()


class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()


class ItemResource(ModelResource):
    class Meta:
        queryset = Item.objects.all()


class BagResource(ModelResource):
    class Meta:
        queryset = Bag.objects.all()


class BagActionResource(ModelResource):
    class Meta:
        queryset = BagAction.objects.all()


class MachineResource(ModelResource):
    class Meta:
        queryset = Machine.objects.all()