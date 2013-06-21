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
    url(r'^api/', include(v1_api.urls)),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect': '/password_reset_done/', 'template_name': 'password_reset_form.html', 'email_template_name': 'password_reset_email.html'}, name='password_reset'),
    url(r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': '/password_done/', 'template_name': 'password_reset_confirm.html'}),
    url(r'^password_done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_complete.html'}, name='password_done'),
)

urlpatterns += patterns('invapp.views',
    url(r'^$', 'home', name='home'),
    url(r'^collection/(?P<id>\w{5}/\w{10,12})$', 'collection',
        name='collection'),
    url(r'^project/(?P<id>\w{5}/\w{10,12})$', 'project', name='project'),
    url(r'^item/(?P<id>\w{5}/\w{9,12})$', 'item', name='item'),
    url(r'^bag/(?P<bagname>.*)$', 'bag', name='bag'),
    url(r'^machine/(?P<id>\w+)$', 'machine', name='machine'),
    url(r'^login/$', 'login_user', name='login'),
    url(r'^logout/$', 'logout_user', name='logout'),
    url(r'^change_password/$', 'change_password', name='change_password'),
    url(r'^change_password_done/$', 'change_password_done', name='change_password_done'),
    url(r'^ajax/collection_items_autocomplete/$', 'collection_items_autocomplete', name='collection_items_autocomplete'),
    url(r'^ajax/search_collection_autocomplete/$', 'search_collection_autocomplete', name='search_collection_autocomplete'),
)
