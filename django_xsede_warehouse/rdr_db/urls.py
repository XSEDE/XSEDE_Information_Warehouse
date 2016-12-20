from django.conf.urls import patterns, include, url
from rdr_db.views import *
from rdr_db.views_v2 import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^v1/rdr-xup/$',
        RDRResource_XUP_List.as_view(),
        name='rdr-xup-list'),
    url(r'^v1/rdr-xup/ID/(?P<id>[^/]+)/$',
        RDRResource_XUP_Detail.as_view(),
        name='rdr-xup-detail'),
    url(r'^v2/rdr-xup/$',
       RDRResource_XUP_v2_List.as_view(),
       name='rdr-xup-list'),
#   url(r'^v3/rdr-xup/$',
#       RDRResource_XUP_v3_List.as_view(),
#       name='rdr-xup-list'),

#   url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]