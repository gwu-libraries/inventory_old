from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'inv.views.home', name='home'),
    # url(r'^inv/', include('inv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('invapp',
    url(r'^$', 'home', name='home'),
    url(r'^collection/(?P<pid>\w{5}/\w{10,12})$', 'collection',
        name='collection'),
    url(r'^project/(?P<pid>\w{5}/\w{10,12})$', 'project', name='project'),
    url(r'^item/(?P<pid>\w{5}/\w{10,12})$', 'item', name='tem'),
    url(r'^bag/(?P<bagid>\w{5}/\w{15,19})$', 'collection', name='bag'),
)
