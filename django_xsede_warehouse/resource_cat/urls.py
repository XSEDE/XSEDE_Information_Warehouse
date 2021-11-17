from django.urls import include, path
from resource_cat.views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
# Special reg for resource/id/<id> in case there are slashes in the 'id'
urlpatterns = [
    path(r'resource_search/affiliation/<str:affiliation>/',
        Resource_Search.as_view(),
        name='resource-search'),
    path(r'resource_search/',
        Resource_Search.as_view(),
        name='resource-search'),
    path(r'providers/affiliation/<str:affiliation>/',
        cache_page(60 * 60)(Resource_Provider_List.as_view()),
        name='resource-provider-list'),
    path(r'providers/',
        cache_page(60 * 60)(Resource_Provider_List.as_view()),
        name='resource-provider-list'),
    path(r'resource_types/affiliation/<str:affiliation>/',
        cache_page(60 * 60)(Resource_Types_List.as_view()),
        name='resource-types-list'),
    path(r'resource_types/',
        cache_page(60 * 60)(Resource_Types_List.as_view()),
        name='resource-types-list'),
    path(r'events/affiliation/<str:affiliation>/',
        cache_page(60 * 5)(Events_List.as_view()),
        name='events-list'),
    path(r'events/',
        cache_page(60 * 5)(Events_List.as_view()),
        name='events-list'),
    path(r'resource/id/<str:id>/',
        Resource_Detail.as_view(),
        name='resource-detail'),
    path(r'resource/id/<str:id>)/',
        Resource_Detail.as_view(),
        name='resource-detail'),
    path(r'resource/',
        Resource_Detail.as_view(),
        name='resource-detail'),
    path(r'resource/affiliation/<str:affiliation>/localid/<str:localid>/',
        Resource_Detail.as_view(),
        name='resource-detail'),
]
