from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from invapp.models import *


class MachineResource(ModelResource):
    class Meta:
        queryset = Machine.objects.all()
        filtering = {
            'name': ALL_WITH_RELATIONS,
            'url': ALL_WITH_RELATIONS
        }


class CollectionResource(ModelResource):
    class Meta:
        queryset = Collection.objects.all()
        filtering = {
            'pid': 'exact',
            'name': ALL_WITH_RELATIONS,
            'created': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'manager': ALL_WITH_RELATIONS
        }


class ProjectResource(ModelResource):
    collection = fields.ForeignKey(CollectionResource, 'collection')

    class Meta:
        queryset = Project.objects.all()
        filtering = {
            'pid': 'exact',
            'created': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'manager': ALL_WITH_RELATIONS,
            'start_date': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'end_date': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }


class ItemResource(ModelResource):
    collection = fields.ForeignKey(CollectionResource, 'collection')
    project = fields.ForeignKey(ProjectResource, 'project')

    class Meta:
        queryset = Item.objects.all()
        filtering = {
            'pid': 'exact',
            'title': ALL_WITH_RELATIONS,
            'local_id': ALL,
            'created': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'original_item_type': ALL,
            'rawfiles_loc': ALL_WITH_RELATIONS,
            'qcfiles_loc': ALL_WITH_RELATIONS,
            'qafiles_loc': ALL_WITH_RELATIONS,
            'finfiles_loc': ALL_WITH_RELATIONS,
            'ocrfiles_loc': ALL_WITH_RELATIONS,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class BagResource(ModelResource):
    item = fields.ForeignKey(ItemResource, 'item')
    machine = fields.ForeignKey(MachineResource, 'machine')

    class Meta:
        queryset = Bag.objects.all()
        filtering = {
            'bagname': ALL_WITH_RELATIONS,
            'created': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'path': 'ALL_WITH_RELATIONS',
            'bag_type': ALL,
            'urlpath': ALL_WITH_RELATIONS,
        }



class BagActionResource(ModelResource):
    bag = fields.ForeignKey(BagResource, 'bag')

    class Meta:
        queryset = BagAction.objects.all()
        filtering = {
            'timestamp': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'action': ALL,
        }