from django.urls import include, path
from monitoring_views_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'software-status/', Software_List.as_view(), name='software-status-list'),
    path(r'software-status/ResourceID/<str:resourceid>/', Software_List.as_view(), name='software-status-list-byresource'),
    path(r'software-status/ID/<str:id>/', Software_Detail.as_view(), name='software-status-detail'),
    path(r'services-status/', Service_List.as_view(), name='services-status-list'),
    path(r'services-status/ResourceID/<str:resourceid>/', Service_List.as_view(), name='services-status-list-byresource'),
    path(r'services-status/ID/<str:id>/', Service_Detail.as_view(), name='services-status-detail'),
]
