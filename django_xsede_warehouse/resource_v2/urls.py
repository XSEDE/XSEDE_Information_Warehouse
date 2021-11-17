from django.urls import include, path
from resource_v2.views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
# Special reg for resource/id/<id> in case there are slashes in the 'id'
urlpatterns = [
    path(r'providers/',
        cache_page(60 * 60)(Resource_Provider_List.as_view()),
        name='resource-provider-list'),
    path(r'resource_search/',
        Resource_Search.as_view(),
        name='resource-search'),
    path(r'resource/id/<str:id>/',
        Resource_Detail.as_view(),
        name='resource-detail'),
    path(r'resource/affiliation/<str:affiliation>/localid/<str:localid>/',
        Resource_Detail.as_view(),
        name='resource-detail'),
    path(r'resource_types/',
        cache_page(60 * 60)(Resource_Types_List.as_view()),
        name='resource-types-list'),
    path(r'event_search/',
        cache_page(60 * 5)(Event_Search.as_view()),
        name='event-search'),
    path(r'guide_search/',
        Guide_Search.as_view(),
        name='guide-search'),
    path(r'guide/id/<str:id>/',
        Guide_Detail.as_view(),
        name='guide-detail'),
    path(r'guide/affiliation/<str:affiliation>/localid/<str:localid>/',
        Guide_Detail.as_view(),
        name='resource-detail'),
]
