from django.conf.urls import patterns, include, url
from django.contrib import admin

from invapp.api import *


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(MachineResource().urls)),
    url(r'^api/', include(CollectionResource().urls)),
    url(r'^api/', include(ProjectResource().urls)),
    url(r'^api/', include(ItemResource().urls)),
    url(r'^api/', include(BagResource().urls)),
    url(r'^api/', include(BagActionResource().urls)),
)

urlpatterns += patterns('invapp.views',
    url(r'^$', 'home', name='home'),
    url(r'^collection/(?P<pid>\w{5}/\w{10,12})$', 'collection',
        name='collection'),
    url(r'^project/(?P<pid>\w{5}/\w{10,12})$', 'project', name='project'),
    url(r'^item/(?P<pid>\w{5}/\w{9,12})$', 'item', name='item'),
    url(r'^bag/(?P<bagname>.*)$', 'bag', name='bag'),
)
