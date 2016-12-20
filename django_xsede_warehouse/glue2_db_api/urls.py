from django.conf.urls import patterns, include, url
from glue2_db_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^applicationenvironment/$',
        ApplicationEnvironment_DbList.as_view(),
        name='applicationenvironment-dblist'),
    url(r'^applicationenvironment/ID/(?P<pk>[^/]+)/$',
        ApplicationEnvironment_DbDetail.as_view(),
        name='applicationenvironment-detail'),

    url(r'^applicationhandle/$',
        ApplicationHandle_DbList.as_view(),
        name='applicationhandle-dblist'),
    url(r'^applicationhandle/ID/(?P<pk>[^/]+)/$',
        ApplicationHandle_DbDetail.as_view(),
        name='applicationhandle-detail'),

    url(r'^abstractservice/$',
        AbstractService_DbList.as_view(),
        name='abstractservice-dblist'),
    url(r'^abstractservice/ID/(?P<pk>[^/]+)/$',
        AbstractService_DbDetail.as_view(),
        name='abstractservice-detail'),

    url(r'^endpoint/$',
        Endpoint_DbList.as_view(),
        name='abstractservice-dblist'),
    url(r'^endpoint/ID/(?P<pk>[^/]+)/$',
        Endpoint_DbDetail.as_view(),
        name='endpoint-detail'),

    url(r'^computingmanager/$',
        ComputingManager_DbList.as_view(),
        name='computingmanager-dblist'),
    url(r'^computingmanager/ID/(?P<pk>[^/]+)/$',
        ComputingManager_DbDetail.as_view(),
        name='computingmanager-detail'),
               
    url(r'^executionenvironment/$',
        ExecutionEnvironment_DbList.as_view(),
        name='executionenvironment-dblist'),
    url(r'^executionenvironment/ID/(?P<pk>[^/]+)/$',
        ExecutionEnvironment_DbDetail.as_view(),
        name='executionenvironment-detail'),

    url(r'^location/$',
        Location_DbList.as_view(),
        name='location-dblist'),
    url(r'^location/ID/(?P<pk>[^/]+)/$',
        Location_DbDetail.as_view(),
        name='location-detail'),

    url(r'^computingshare/$',
        ComputingShare_DbList.as_view(),
        name='computingshare-dblist'),
    url(r'^computingshare/ID/(?P<pk>[^/]+)/$',
        ComputingShare_DbDetail.as_view(),
        name='computingshare-detail'),

    url(r'^computingactivity/$',
        ComputingActivity_DbList.as_view(),
        name='computingactivity-dblist'),
    url(r'^computingactivity/ID/(?P<pk>[^/]+)/$',
        ComputingActivity_DbDetail.as_view(),
        name='computingactivity-detail'),

#    url(r'^entityhistory/$',
#        EntityHistory_DbList.as_view(),
#        name='entityhistory-dblist'),
    url(r'^entityhistory/ID/(?P<id>[^/]+)/$',
        EntityHistory_DbDetail.as_view(),
        name='entityhistory-detail'),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
