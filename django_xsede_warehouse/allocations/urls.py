from django.conf.urls import include, url
from allocations.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^resources/$', AllocationResources_List.as_view(), name='allocationresources-list'),
    url(r'^resources/ResourceID/(?P<ResourceID>[^/]+)/$', AllocationResources_List.as_view(), name='allocationresources-byresource'),
    url(r'^resources/project_number/(?P<project_number>[^/]+)/$', AllocationResources_List.as_view(), name='allocationresources-byproject'),
]
