from django.conf.urls import include, url
from views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^software-status/$', Software_List.as_view(), name='software-status-list'),
    url(r'^software-status/ID/(?P<id>[^/]+)/$', Software_Detail.as_view(), name='software-status-detail'),
    url(r'^software-status/ResourceID/(?P<resourceid>[^/]+)/$', Software_Detail.as_view(), name='software-status-detail'),
    url(r'^services-status/$', Service_List.as_view(), name='services-status-list'),
    url(r'^services-status/ID/(?P<id>[^/]+)/$', Service_Detail.as_view(), name='services-status-detail'),
    url(r'^services-status/ResourceID/(?P<resourceid>[^/]+)/$', Service_Detail.as_view(), name='services-status-detail'),
]
