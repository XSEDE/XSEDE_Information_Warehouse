from django.conf.urls import include, url
from glue2_db_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^admindomain/$', AdminDomain_DbList.as_view(), name='admindomain-dblist'),
    url(r'^admindomain/ID/(?P<pk>[^/]+)/$', AdminDomain_DbDetail.as_view(), name='admindomain-detail'),

    url(r'^userdomain/$', UserDomain_DbList.as_view(), name='userdomain-dblist'),
    url(r'^userdomain/ID/(?P<pk>[^/]+)/$', UserDomain_DbDetail.as_view(), name='userdomain-detail'),

    url(r'^accesspolicy/$', AccessPolicy_DbList.as_view(), name='accesspolicy-dblist'),
    url(r'^accesspolicy/ID/(?P<pk>[^/]+)/$', AccessPolicy_DbDetail.as_view(), name='accesspolicy-detail'),

    url(r'^contact/$', Contact_DbList.as_view(), name='contact-dblist'),
    url(r'^contact/ID/(?P<pk>[^/]+)/$', Contact_DbDetail.as_view(), name='contact-detail'),

    url(r'^location/$', Location_DbList.as_view(), name='location-dblist'),
    url(r'^location/ID/(?P<pk>[^/]+)/$', Location_DbDetail.as_view(), name='location-detail'),

    url(r'^applicationenvironment/$', ApplicationEnvironment_DbList.as_view(), name='applicationenvironment-dblist'),
    url(r'^applicationenvironment/ID/(?P<pk>[^/]+)/$', ApplicationEnvironment_DbDetail.as_view(), name='applicationenvironment-detail'),

    url(r'^applicationhandle/$', ApplicationHandle_DbList.as_view(), name='applicationhandle-dblist'),
    url(r'^applicationhandle/ID/(?P<pk>[^/]+)/$', ApplicationHandle_DbDetail.as_view(), name='applicationhandle-detail'),

    url(r'^abstractservice/$', AbstractService_DbList.as_view(), name='abstractservice-dblist'),
    url(r'^abstractservice/ID/(?P<pk>[^/]+)/$', AbstractService_DbDetail.as_view(), name='abstractservice-detail'),

    url(r'^endpoint/$', Endpoint_DbList.as_view(), name='abstractservice-dblist'),
    url(r'^endpoint/ID/(?P<pk>[^/]+)/$', Endpoint_DbDetail.as_view(), name='endpoint-detail'),

    url(r'^computingmanager/$', ComputingManager_DbList.as_view(), name='computingmanager-dblist'),
    url(r'^computingmanager/ID/(?P<pk>[^/]+)/$', ComputingManager_DbDetail.as_view(), name='computingmanager-detail'),
               
    url(r'^computingshare/$', ComputingShare_DbList.as_view(), name='computingshare-dblist'),
    url(r'^computingshare/ID/(?P<pk>[^/]+)/$', ComputingShare_DbDetail.as_view(), name='computingshare-detail'),

    url(r'^executionenvironment/$', ExecutionEnvironment_DbList.as_view(), name='executionenvironment-dblist'),
    url(r'^executionenvironment/ID/(?P<pk>[^/]+)/$', ExecutionEnvironment_DbDetail.as_view(), name='executionenvironment-detail'),

    url(r'^computingqueue/$', ComputingQueue_DbList.as_view(), name='computingqueue-dblist'),
    url(r'^computingqueue/ResourceID/(?P<resourceid>[^/]+)/$', ComputingQueue_DbList.as_view(), name='computingqueue-dblist'),
    url(r'^computingqueue/ID/(?P<pk>[^/]+)/$', ComputingQueue_DbDetail.as_view(), name='computingqueue-detail'),

    url(r'^computingactivity/$', ComputingActivity_DbList.as_view(), name='computingactivity-dblist'),
    url(r'^computingactivity/ID/(?P<pk>[^/]+)/$', ComputingActivity_DbDetail.as_view(), name='computingactivity-detail'),

    url(r'^computingmanageracceleratorinfo/$', ComputingManagerAcceleratorInfo_DbList.as_view(), name='computingmanageracceleratorinfo-dblist'),
    url(r'^computingmanageracceleratorinfo/ID/(?P<pk>[^/]+)/$', ComputingManagerAcceleratorInfo_DbDetail.as_view(), name='computingmanageracceleratorinfo-detail'),

    url(r'^computingshareacceleratorinfo/$', ComputingShareAcceleratorInfo_DbList.as_view(), name='computingshareacceleratorinfo-dblist'),
    url(r'^computingshareacceleratorinfo/ID/(?P<pk>[^/]+)/$', ComputingShareAcceleratorInfo_DbDetail.as_view(), name='computingshareacceleratorinfo-detail'),

    url(r'^acceleratorenvironment/$', AcceleratorEnvironment_DbList.as_view(), name='acceleratorenvironment-dblist'),
    url(r'^acceleratorenvironment/ID/(?P<pk>[^/]+)/$', AcceleratorEnvironment_DbDetail.as_view(), name='acceleratorenvironment-detail'),

    url(r'^entityhistory/ID/(?P<id>[^/]+)/$', EntityHistory_DbDetail.as_view(), name='entityhistory-detail'),
]
#  Disable because it causes problems, JP 2018-05-16
#url(r'^entityhistory/doctype/(?P<doctype>[^/]+)/$', EntityHistory_DbList.as_view(), name='entityhistory-dblist'),
