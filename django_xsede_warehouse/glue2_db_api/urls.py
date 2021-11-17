from django.urls import include, path
from glue2_db_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'admindomain/', AdminDomain_DbList.as_view(), name='admindomain-dblist'),
    path(r'admindomain/ID/<str:pk>/', AdminDomain_DbDetail.as_view(), name='admindomain-detail'),

    path(r'userdomain/', UserDomain_DbList.as_view(), name='userdomain-dblist'),
    path(r'userdomain/ID/<str:pk>/', UserDomain_DbDetail.as_view(), name='userdomain-detail'),

    path(r'accesspolicy/', AccessPolicy_DbList.as_view(), name='accesspolicy-dblist'),
    path(r'accesspolicy/ID/<str:pk>/', AccessPolicy_DbDetail.as_view(), name='accesspolicy-detail'),

    path(r'contact/', Contact_DbList.as_view(), name='contact-dblist'),
    path(r'contact/ID/<str:pk>/', Contact_DbDetail.as_view(), name='contact-detail'),

    path(r'location/', Location_DbList.as_view(), name='location-dblist'),
    path(r'location/ID/<str:pk>/', Location_DbDetail.as_view(), name='location-detail'),

    path(r'applicationenvironment/', ApplicationEnvironment_DbList.as_view(), name='applicationenvironment-dblist'),
    path(r'applicationenvironment/ID/<str:pk>/', ApplicationEnvironment_DbDetail.as_view(), name='applicationenvironment-detail'),

    path(r'applicationhandle/', ApplicationHandle_DbList.as_view(), name='applicationhandle-dblist'),
    path(r'applicationhandle/ID/<str:pk>/', ApplicationHandle_DbDetail.as_view(), name='applicationhandle-detail'),

    path(r'abstractservice/', AbstractService_DbList.as_view(), name='abstractservice-dblist'),
    path(r'abstractservice/ID/<str:pk>/', AbstractService_DbDetail.as_view(), name='abstractservice-detail'),

    path(r'endpoint/', Endpoint_DbList.as_view(), name='abstractservice-dblist'),
    path(r'endpoint/ID/<str:pk>/', Endpoint_DbDetail.as_view(), name='endpoint-detail'),

    path(r'computingmanager/', ComputingManager_DbList.as_view(), name='computingmanager-dblist'),
    path(r'computingmanager/ID/<str:pk>/', ComputingManager_DbDetail.as_view(), name='computingmanager-detail'),
               
    path(r'computingshare/', ComputingShare_DbList.as_view(), name='computingshare-dblist'),
    path(r'computingshare/ID/<str:pk>/', ComputingShare_DbDetail.as_view(), name='computingshare-detail'),

    path(r'executionenvironment/', ExecutionEnvironment_DbList.as_view(), name='executionenvironment-dblist'),
    path(r'executionenvironment/ID/<str:pk>/', ExecutionEnvironment_DbDetail.as_view(), name='executionenvironment-detail'),

    path(r'computingqueue/', ComputingQueue_DbList.as_view(), name='computingqueue-dblist'),
    path(r'computingqueue/ResourceID/<str:resourceid>/', ComputingQueue_DbList.as_view(), name='computingqueue-dblist'),
    path(r'computingqueue/ID/<str:pk>/', ComputingQueue_DbDetail.as_view(), name='computingqueue-detail'),

    path(r'computingactivity/', ComputingActivity_DbList.as_view(), name='computingactivity-dblist'),
    path(r'computingactivity/ID/<str:pk>/', ComputingActivity_DbDetail.as_view(), name='computingactivity-detail'),

    path(r'computingmanageracceleratorinfo/', ComputingManagerAcceleratorInfo_DbList.as_view(), name='computingmanageracceleratorinfo-dblist'),
    path(r'computingmanageracceleratorinfo/ID/<str:pk>/', ComputingManagerAcceleratorInfo_DbDetail.as_view(), name='computingmanageracceleratorinfo-detail'),

    path(r'computingshareacceleratorinfo/', ComputingShareAcceleratorInfo_DbList.as_view(), name='computingshareacceleratorinfo-dblist'),
    path(r'computingshareacceleratorinfo/ID/<str:pk>/', ComputingShareAcceleratorInfo_DbDetail.as_view(), name='computingshareacceleratorinfo-detail'),

    path(r'acceleratorenvironment/', AcceleratorEnvironment_DbList.as_view(), name='acceleratorenvironment-dblist'),
    path(r'acceleratorenvironment/ID/<str:pk>/', AcceleratorEnvironment_DbDetail.as_view(), name='acceleratorenvironment-detail'),

    path(r'entityhistory/ID/<str:id>/', EntityHistory_DbDetail.as_view(), name='entityhistory-detail'),
]
#  Disable because it causes problems, JP 2018-05-16
#path(r'^entityhistory/doctype/(?P<doctype>[^/]+)/$', EntityHistory_DbList.as_view(), name='entityhistory-dblist'),
