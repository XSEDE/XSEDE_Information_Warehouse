from django.urls import include, path
from projectresources.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'projectresources/', ProjectResource_List.as_view(), name='projectresources-list'),
    path(r'projectresources/ResourceID/<str:ResourceID>/', ProjectResource_By_Resource.as_view(), name='projectresources-by-resource'),
    path(r'projectresources/project_number/<str:project_number>/', ProjectResource_By_Number.as_view(), name='projectresources-by-number'),
]
