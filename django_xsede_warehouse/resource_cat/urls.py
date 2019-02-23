from django.conf.urls import include, url
from resource_cat.views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^resource_search/affiliation/(?P<affiliation>[^/]+)/?$',
        Resource_Search.as_view(),
        name='resource-search'),
    url(r'^resource_search/?$',
        Resource_Search.as_view(),
        name='resource-search'),
    url(r'^providers/affiliation/(?P<affiliation>[^/]+)/?$',
        cache_page(60 * 60)(Resource_Provider_List.as_view()),
        name='resource-provider-list'),
    url(r'^providers/?$',
        cache_page(60 * 60)(Resource_Provider_List.as_view()),
        name='resource-provider-list'),
    url(r'^resource_types/affiliation/(?P<affiliation>[^/]+)/?$',
        cache_page(60 * 60)(Resource_Types_List.as_view()),
        name='resource-types-list'),
    url(r'^resource_types/?$',
        cache_page(60 * 60)(Resource_Types_List.as_view()),
        name='resource-types-list'),
    url(r'^events/affiliation/(?P<affiliation>[^/]+)/?$',
        cache_page(60 * 5)(Events_List.as_view()),
        name='events-list'),
    url(r'^events/?$',
        cache_page(60 * 5)(Events_List.as_view()),
        name='events-list'),
    url(r'^resource/id/(?P<id>[^/]+)/?$',
        Resource_Detail.as_view(),
        name='resource-detail'),
    url(r'^resource/affiliation/(?P<affiliation>[^/]+)/localid/(?P<localid>[^/]+)/?$',
        Resource_Detail.as_view(),
        name='resource-detail'),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
