from django.conf.urls import include, url
from speedpage.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^speedpage/$',
        speedpage_List.as_view(),
        name='speedpage-list'),
    url(r'^speedpage/sourceid/(?P<sourceid>[^/]+)/destid/(?P<destid>[^/]+)/$',
        speedpage_Detail.as_view(),
        name='speedpage-sourcedest'),
    url(r'^speedpage/sourceid/(?P<sourceid>[^/]+)/$',
        speedpage_Detail.as_view(),
        name='speedpage-sourceid'),
    url(r'^speedpage/destid/(?P<destid>[^/]+)/$',
        speedpage_Detail.as_view(),
        name='speedpage-destid'),

#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
