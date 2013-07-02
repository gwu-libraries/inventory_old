from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication, \
    MultiAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization
from invapp.models import Machine, Collection, Project, Item, Bag, BagAction


class MachineResource(ModelResource):
    class Meta:
        queryset = Machine.objects.all()
        filtering = {
            'name': ALL_WITH_RELATIONS,
            'url': ALL_WITH_RELATIONS,
            'ip': ALL_WITH_RELATIONS,
            'notes': ALL_WITH_RELATIONS
        }
        authentication = MultiAuthentication(ApiKeyAuthentication(),
            Authentication())
        authorization = DjangoAuthorization()


class CollectionResource(ModelResource):
    class Meta:
        queryset = Collection.objects.all()
        filtering = {
            'id': 'exact',
            'name': ALL_WITH_RELATIONS,
            'created': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'manager': ALL_WITH_RELATIONS
        }
        authentication = MultiAuthentication(ApiKeyAuthentication(),
            Authentication())
        authorization = DjangoAuthorization()


class ProjectResource(ModelResource):
    collection = fields.ForeignKey(CollectionResource, 'collection', null=True,
        blank=True)

    class Meta:
        queryset = Project.objects.all()
        filtering = {
            'id': 'exact',
            'name': ALL_WITH_RELATIONS,
            'created': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'collection': 'exact'
        }
        authentication = MultiAuthentication(ApiKeyAuthentication(),
            Authentication())
        authorization = DjangoAuthorization()


class ItemResource(ModelResource):
    collection = fields.ForeignKey(CollectionResource, 'collection', null=True,
        blank=True)
    project = fields.ForeignKey(ProjectResource, 'project', null=True,
        blank=True)

    class Meta:
        queryset = Item.objects.all()
        filtering = {
            'id': 'exact',
            'title': ALL_WITH_RELATIONS,
            'local_id': ALL,
            'collection': 'exact',
            'project': 'exact',
            'created': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'original_item_type': ALL,
            'notes': ALL_WITH_RELATIONS
        }
        authentication = MultiAuthentication(ApiKeyAuthentication(),
            Authentication())
        authorization = DjangoAuthorization()


class BagResource(ModelResource):
    item = fields.ForeignKey(ItemResource, 'item')
    machine = fields.ForeignKey(MachineResource, 'machine')

    class Meta:
        queryset = Bag.objects.all()
        filtering = {
            'bagname': ALL_WITH_RELATIONS,
            'created': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'machine': 'exact',
            'item': 'exact',
            'path': 'ALL_WITH_RELATIONS',
            'bag_type': ALL,
        }
        authentication = MultiAuthentication(ApiKeyAuthentication(),
            Authentication())
        authorization = DjangoAuthorization()

    def dehydrate_payload(self, bundle):
        return bundle.obj.list_payload()


class BagActionResource(ModelResource):
    bag = fields.ForeignKey(BagResource, 'bag')

    class Meta:
        queryset = BagAction.objects.all()
        filtering = {
            'bag': 'exact',
            'timestamp': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'action': ALL,
            'note': ALL_WITH_RELATIONS
        }
        authentication = MultiAuthentication(ApiKeyAuthentication(),
            Authentication())
        authorization = DjangoAuthorization()
