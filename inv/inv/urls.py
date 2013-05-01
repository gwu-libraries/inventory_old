from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from invapp.api.resources import *


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(MachineResource())
v1_api.register(CollectionResource())
v1_api.register(ProjectResource())
v1_api.register(ItemResource())
v1_api.register(BagResource())
v1_api.register(BagActionResource())


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls))
)

urlpatterns += patterns('invapp.views',
    url(r'^$', 'home', name='home'),
    url(r'^collection/(?P<id>\w{5}/\w{10,12})$', 'collection',
        name='collection'),
    url(r'^project/(?P<id>\w{5}/\w{10,12})$', 'project', name='project'),
    url(r'^item/(?P<id>\w{5}/\w{9,12})$', 'item', name='item'),
    url(r'^bag/(?P<bagname>.*)$', 'bag', name='bag'),
)
