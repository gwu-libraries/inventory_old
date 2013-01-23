from django.contrib import admin
from invapp.models import *
from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(ApiKey)
admin.site.register(ApiAccess)

class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)

admin.site.register(Collection)
admin.site.register(Project)
admin.site.register(Item)
admin.site.register(Bag)
admin.site.register(BagAction)