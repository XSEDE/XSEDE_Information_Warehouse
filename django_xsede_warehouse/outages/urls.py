from django.conf.urls import patterns, include, url
from outages.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^outages/$',
        Outages_List.as_view(),
        name='outages-list'),
    url(r'^outages/ID/(?P<id>[^/]+)/$',
        Outages_Detail.as_view(),
        name='outages-detail'),
    url(r'^outages/ResourceID/(?P<ResourceID>[^/]+)/$',
        Outages_By_Resource.as_view(),
        name='outages-by-resource'),
    url(r'^outages/Current/$',
        Outages_Current.as_view(),
        name='outages-current'),
    url(r'^outages/Past/$',
        Outages_Past.as_view(),
        name='outages-past'),
    url(r'^outages/Future/$',
        Outages_Future.as_view(),
        name='outages-future'),
    url(r'^outages/StatusRelevant/ResourceID/(?P<ResourceID>[^/]+)/$',
        Outages_StatusRelevant.as_view(),
        name='outages-statusrelevant'),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
