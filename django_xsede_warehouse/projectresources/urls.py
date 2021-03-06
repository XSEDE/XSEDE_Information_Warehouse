from django.conf.urls import include, url
from projectresources.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^projectresources/$', ProjectResource_List.as_view(), name='projectresources-list'),
    url(r'^projectresources/ResourceID/(?P<ResourceID>[^/]+)/$', ProjectResource_By_Resource.as_view(), name='projectresources-by-resource'),
    url(r'^projectresources/project_number/(?P<project_number>[^/]+)/$', ProjectResource_By_Number.as_view(), name='projectresources-by-number'),
]
