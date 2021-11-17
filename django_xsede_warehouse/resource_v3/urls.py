from django.urls import include, path
from .views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
# Special reg for resource/id/<id> in case there are slashes in the 'id'
urlpatterns = [
    path(r'catalog_search/',
        Catalog_Search.as_view(), name='catalog-search'),
    path(r'catalog/id/<str:id>/',
        Catalog_Detail.as_view(), name='catalog-detail'),
    path(r'local/id/<str:id>/',
        Local_Detail.as_view(), name='local-detail-globalid'),
    path(r'local_search/',
        Local_Search.as_view(), name='local-search'),
    path(r'resource_types/',
        cache_page(60 * 60)(Resource_Types_List.as_view()), name='resource-types-list'),
    path(r'resource/id/<str:id>/',
        Resource_Detail.as_view(), name='resource-detail'),
    path(r'resource_search/',
        Resource_Search.as_view(), name='resource-search'),
    path(r'resource_esearch/',
        Resource_ESearch.as_view(), name='resource-esearch'),
    path(r'event/id/<str:id>/',
        Event_Detail.as_view(), name='event-detail'),
    path(r'event_search/',
        Event_Search.as_view(), name='event-search'),
]
