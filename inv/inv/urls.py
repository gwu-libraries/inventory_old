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

# BASIC SITE PAGES
urlpatterns += patterns('invapp',
    url(r'^$', 'home', name='home'),
    url(r'^browse/(?P<plural_otype>[a-z]+)$', 'browse', name='browse'),
    url(r'^about$', 'about', name='about'),
    url(r'^robots.txt$', 'robots', name='robots'),
)

# BASIC CRUD OPERATIONS
urlpatterns += patterns('invapp',
    url(r'^(?P<otype>[a-z]+)/new', 'create', name='create'),
    url(r'^(?P<otype>[a-z]+)/(?P<pid>\w+)$', 'read', name='read'),
    url(r'^(?P<otype>[a-z]+)/(?P<pid>\w+)/edit$', 'update', name='update'),
    url(r'^(?P<otype>[a-z]+)/(?P<pid>\w+)/delete$', 'delete', name='delete'),
)
