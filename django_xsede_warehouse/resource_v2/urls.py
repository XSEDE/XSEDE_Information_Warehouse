from django.conf.urls import include, url
from resource_v2.views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
# Special reg for resource/id/<id> in case there are slashes in the 'id'
urlpatterns = [
    url(r'^providers/?$',
        cache_page(60 * 60)(Resource_Provider_List.as_view()),
        name='resource-provider-list'),
    url(r'^resource_search/?$',
        Resource_Search.as_view(),
        name='resource-search'),
    url(r'^resource/id/(?P<id>.+)/$',
        Resource_Detail.as_view(),
        name='resource-detail'),
    url(r'^resource/affiliation/(?P<affiliation>[^/]+)/localid/(?P<localid>[^/]+)/?$',
        Resource_Detail.as_view(),
        name='resource-detail'),
    url(r'^resource_types/?$',
        cache_page(60 * 60)(Resource_Types_List.as_view()),
        name='resource-types-list'),
    url(r'^event_search/?$',
        cache_page(60 * 5)(Event_Search.as_view()),
        name='event-search'),
    url(r'^guide_search/?$',
        Guide_Search.as_view(),
        name='guide-search'),
    url(r'^guide/id/(?P<id>.+)/$',
        Guide_Detail.as_view(),
        name='guide-detail'),
    url(r'^guide/affiliation/(?P<affiliation>[^/]+)/localid/(?P<localid>[^/]+)/?$',
        Guide_Detail.as_view(),
        name='resource-detail'),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
