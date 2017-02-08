from django.conf.urls import patterns, include, url
from warehouse_views.views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^v1/resources/$',
        Resource_List.as_view(),
        name='resource-list'),
    url(r'^v1/resources-active/$',
        Resource_List_Active.as_view(),
        name='resource-list-active'),
    url(r'^v1/resources-xdcdb-active/$',
        Resource_List_XDCDB_Active.as_view(),
        name='resource-list-active-xdcdb'),
    url(r'^v1/resource/ResourceID/(?P<resourceid>[^/]+)/$',
        Resource_Detail.as_view(),
        name='resource-detail'),
              
    url(r'^v1/software/$',
        Software_Full.as_view(),
        name='software-list'),
    url(r'^v1/software/ID/(?P<id>[^/]+)/$',
        Software_Full.as_view(),
        name='software-detail'),
    url(r'^v1/software/ResourceID/(?P<resourceid>[^/]+)/$',
        Software_Full.as_view(),
        name='software-detail'),
    url(r'^v1/software/AppName/(?P<appname>[^/]+)/$',
        Software_Full.as_view(),
        name='software-detail'),
               
    url(r'^v1/software-xup/$',
        Software_XUP_v1_List.as_view(),
        name='software-xup-list'),

    url(r'^v1/software-cached/$',
        cache_page(60 * 15)(Software_Full.as_view()),
        name='software-cache-list'),

#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
