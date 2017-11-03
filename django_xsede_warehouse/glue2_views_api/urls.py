from django.conf.urls import include, url
from glue2_views_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
#    url(r'^applicationenvironment/$',
#        ApplicationEnvironment_List.as_view(),
#        name='applicationenvironment-list'),
    url(r'^software/$', Software_List.as_view(), name='software-list'),
    url(r'^software/ID/(?P<id>[^/]+)/$', Software_Detail.as_view(), name='software-detail'),
    url(r'^software/ResourceID/(?P<resourceid>[^/]+)/$', Software_Detail.as_view(), name='software-detail'),
    url(r'^software/AppName/(?P<appname>[^/]+)/$', Software_Detail.as_view(), name='software-detail'),
               
    url(r'^software-spf/$', Software_List.as_view(), name='software-list'),
    url(r'^software-spf/ID/(?P<id>[^/]+)/$', Software_Detail.as_view(), name='software-detail'),
    url(r'^software-spf/ResourceID/(?P<resourceid>[^/]+)/$', Software_Detail.as_view(), name='software-detail'),
    url(r'^software-spf/AppName/(?P<appname>[^/]+)/$', Software_Detail.as_view(), name='software-detail'),

    url(r'^services/$', Services_List.as_view(), name='services-list'),
    url(r'^services/ID/(?P<id>[^/]+)/$', Services_Detail.as_view(), name='services-detail'),
    url(r'^services/ResourceID/(?P<resourceid>[^/]+)/$', Services_Detail.as_view(), name='services-detail'),
    url(r'^services/InterfaceName/(?P<interfacename>[^/]+)/$', Services_Detail.as_view(), name='services-detail'),
    url(r'^services/ServiceType/(?P<servicetype>[^/]+)/$', Services_Detail.as_view(), name='services-detail'),

    url(r'^services-spf/$', Services_List.as_view(), name='services-list'),
    url(r'^services-spf/ID/(?P<id>[^/]+)/$', Services_Detail.as_view(), name='services-detail'),
    url(r'^services-spf/ResourceID/(?P<resourceid>[^/]+)/$', Services_Detail.as_view(), name='services-detail'),
    url(r'^services-spf/InterfaceName/(?P<interfacename>[^/]+)/$', Services_Detail.as_view(), name='services-detail'),
    url(r'^services-spf/ServiceType/(?P<servicetype>[^/]+)/$', Services_Detail.as_view(), name='services-detail'),

    url(r'^jobs/$', Jobs_List.as_view(), name='jobs-list'),
    url(r'^jobs/ResourceID/(?P<resourceid>[^/]+)/$', Jobs_List.as_view(), name='jobs-list'),
               
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
