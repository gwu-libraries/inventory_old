from django.contrib import admin
from invapp.models import Machine, Collection, Project, Item, Bag, BagAction
from tastypie.admin import ApiKeyInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]


class MachineAdmin(admin.ModelAdmin):
    fields = ['name', 'url', 'ip', 'notes', 'www_root']
    list_display = ('name', 'url', 'ip', 'www_root')
    search_fields = ['name']


class ProjectAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'collection', 'created']
    list_display = ('id', 'name', 'collection', 'created')
    search_fields = ['name']
    date_hierarchy = 'created'


class BagAdmin(admin.ModelAdmin):
    fields = ('bagname', 'item', 'machine', 'absolute_filesystem_path',
              'bag_type', 'created', 'payload')
    list_display = ('bagname', 'item', 'machine', 'absolute_filesystem_path',
                    'bag_type', 'created')
    search_fields = ['bagname']
    date_hierarchy = 'created'


class CollectionAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'manager', 'description', 'access_loc', 'created']
    list_display = ('id', 'name', 'manager', 'description', 'access_loc',
                    'created')
    search_fields = ['name']
    date_hierarchy = 'created'


class ItemAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'local_id', 'collection', 'project',
              'original_item_type', 'notes', 'access_loc', 'created']
    list_display = ('id', 'title', 'local_id', 'collection', 'project',
                    'original_item_type', 'created')
    search_fields = ['title']
    date_hierarchy = 'created'


class BagActionAdmin(admin.ModelAdmin):
    fields = ['bag', 'timestamp', 'action', 'note']
    list_display = ('bag', 'timestamp', 'action')


admin.site.unregister(User)
admin.site.register(User, UserModelAdmin)

admin.site.register(Machine, MachineAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Bag, BagAdmin)
admin.site.register(BagAction, BagActionAdmin)
