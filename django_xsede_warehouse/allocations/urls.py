from django.urls import include, path
from allocations.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'resources/', AllocationResources_List.as_view(), name='allocationresources-list'),
    path(r'resources/ResourceID/<str:ResourceID>/', AllocationResources_List.as_view(), name='allocationresources-byresource'),
    path(r'resources/project_number/<str:project_number>/', AllocationResources_List.as_view(), name='allocationresources-byproject'),
]
