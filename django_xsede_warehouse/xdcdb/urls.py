from django.conf.urls import patterns, include, url
from xdcdb.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^xdcdb/$',
        TGResource_List.as_view(),
        name='xdcdb-list'),
    url(r'^xdcdb/ID/(?P<id>[^/]+)/$',
        TGResource_Detail.as_view(),
        name='xdcdb-detail'),
    url(r'^xdcdb-pub/ID/(?P<id>[^/]+)/$',
        TGResourcePublished_Detail.as_view(),
        name='xdcdb-pub'),

#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
