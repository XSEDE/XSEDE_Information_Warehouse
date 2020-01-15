from django.conf.urls import include, url
from glue2_db_api.views import *
from goendpoint_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^goservices/$',
        goServices_List.as_view(),
        name='goservices-list'),
    url(r'^goservices/ID/(?P<id>[^/]+)/$',
        goServices_Detail.as_view(),
        name='goservices-detail'),
    url(r'^goservices/ResourceID/(?P<resourceid>[^/]+)/$',
        goServices_Detail.as_view(),
        name='goservices-detail'),
    url(r'^goservices/InterfaceName/(?P<interfacename>[^/]+)/$',
        goServices_Detail.as_view(),
        name='goservices-detail'),
    url(r'^goservices/ServiceType/(?P<servicetype>[^/]+)/$',
        goServices_Detail.as_view(),
        name='goservices-detail'),
]
