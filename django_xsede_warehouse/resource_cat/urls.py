from django.conf.urls import include, url
from resource_cat.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^resource_search/affiliation/(?P<affiliation>[^/]+)/$',
        Resource_Search.as_view(),
        name='resource-search'),
    url(r'^resource_search/$',
        Resource_Search.as_view(),
        name='resource-search'),
    url(r'^providers/affiliation/(?P<affiliation>[^/]+)/$',
        Resource_Provider_List.as_view(),
        name='resource-provider-list'),
    url(r'^providers/$',
        Resource_Provider_List.as_view(),
        name='resource-provider-list'),
    url(r'^events/affiliation/(?P<affiliation>[^/]+)/$',
        Events_List.as_view(),
        name='events-list'),
    url(r'^events/$',
        Events_List.as_view(),
        name='events-list'),
    url(r'^resource/id/(?P<id>[^/]+)/$',
        Resource_Detail.as_view(),
        name='resource-detail'),
    url(r'^resource/affiliation/(?P<affiliation>[^/]+)/localid/(?P<localid>[^/]+)/$',
        Resource_Detail.as_view(),
        name='resource-detail'),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
