from django.conf.urls import include, url
from xdcdb.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^xdcdb/$',
        XcdbResource_List.as_view(),
        name='xdcdb-list'),
    url(r'^xdcdb/ID/(?P<id>[^/]+)/$',
        XcdbResource_Detail.as_view(),
        name='xdcdb-detail'),
    url(r'^xdcdb-pub/ID/(?P<id>[^/]+)/$',
        XcdbResourcePublished_Detail.as_view(),
        name='xdcdb-pub'),

#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
