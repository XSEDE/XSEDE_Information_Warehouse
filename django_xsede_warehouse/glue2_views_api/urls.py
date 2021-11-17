from django.urls import include, path
from glue2_views_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'software/', Software_List.as_view(), name='software-list'),
    path(r'software/ID/<str:id>/', Software_Detail.as_view(), name='software-detail'),
    path(r'software/ResourceID/<str:resourceid>/', Software_Detail.as_view(), name='software-detail'),
    path(r'software/AppName/<str:appname>/', Software_Detail.as_view(), name='software-detail'),
               
    path(r'software-spf/', Software_List.as_view(), name='software-list'),
    path(r'software-spf/ID/<str:id>/', Software_Detail.as_view(), name='software-detail'),
    path(r'software-spf/ResourceID/<str:resourceid>/', Software_Detail.as_view(), name='software-detail'),
    path(r'software-spf/AppName/<str:appname>/', Software_Detail.as_view(), name='software-detail'),

    path(r'services/', Services_List.as_view(), name='services-list'),
    path(r'services/ID/<str:id>/', Services_Detail.as_view(), name='services-detail'),
    path(r'services/ResourceID/<str:resourceid>/', Services_Detail.as_view(), name='services-detail'),
    path(r'services/InterfaceName/<str:interfacename>/', Services_Detail.as_view(), name='services-detail'),
    path(r'services/ServiceType/<str:servicetype>/', Services_Detail.as_view(), name='services-detail'),

    path(r'services-spf/', Services_List.as_view(), name='services-list'),
    path(r'services-spf/ID/<str:id>/', Services_Detail.as_view(), name='services-detail'),
    path(r'services-spf/ResourceID/<str:resourceid>/', Services_Detail.as_view(), name='services-detail'),
    path(r'services-spf/InterfaceName/<str:interfacename>/', Services_Detail.as_view(), name='services-detail'),
    path(r'services-spf/ServiceType/<str:servicetype>/', Services_Detail.as_view(), name='services-detail'),

    path(r'jobqueue/', Jobqueue_List.as_view(), name='jobsqueue-list'),
    path(r'jobqueue/ResourceID/<str:resourceid>/', Jobqueue_List.as_view(), name='jobsqueue-list'),
    path(r'jobs/', Jobqueue_List.as_view(), name='jobsqueue-list'),
    path(r'jobs/ResourceID/<str:resourceid>/', Jobqueue_List.as_view(), name='jobsqueue-list'),
    path(r'jobs2/ID/<str:id>/', Job_Detail.as_view(), name='jobs-detail'),
    path(r'jobs2/ResourceID/<str:resourceid>/', Job_List.as_view(), name='jobs-list'),
    path(r'userjobs/ResourceID/<str:resourceid>/', Jobs_per_Resource_by_ProfileID.as_view(), name='jobs-profileid'),
    path(r'userjobs/', Jobs_by_ProfileID.as_view(), name='jobs-profileid'),
    path(r'jobs2/ResourceID/<str:resourceid>/Queue/<str:queue>/', Job_List.as_view(), name='jobs-list'),
    path(r'jobs2/ResourceID/<str:resourceid>/LocalAccount/<str:localaccount>/', Job_List.as_view(), name='jobs-list'),
]
