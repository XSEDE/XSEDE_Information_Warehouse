from django.urls import include, path
from outages.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'outages/', Outages_List.as_view(), name='outages-list'),
    path(r'outages/ID/<str:id>/', Outages_Detail.as_view(), name='outages-detail'),
    path(r'outages/ResourceID/<str:ResourceID>/', Outages_By_Resource.as_view(), name='outages-by-resource'),
    path(r'outages/Current/', Outages_Current.as_view(), name='outages-current'),
    path(r'outages/Past/', Outages_Past.as_view(), name='outages-past'),
    path(r'outages/Future/', Outages_Future.as_view(), name='outages-future'),
    path(r'outages/StatusRelevant/ResourceID/<str:ResourceID>/', Outages_StatusRelevant.as_view(), name='outages-statusrelevant'),
]
