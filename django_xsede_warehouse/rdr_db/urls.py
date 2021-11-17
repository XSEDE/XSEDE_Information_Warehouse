from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rdr_db.views import *
from rdr_db.views_v2 import *
from rdr_db.views_v3 import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'v1/rdr/', RDRResource_List.as_view(), name='rdr-list'),
    path(r'v1/rdr/ID/<str:id>/', RDRResource_Detail.as_view(), name='rdr-detail'),
    path(r'v1/rdr/ResourceID/<str:resourceid>/', RDRResource_List.as_view(), name='rdr-list-resourceid'),
    path(r'v1/rdr/SiteID/<str:siteid>/', RDRResource_List.as_view(), name='rdr-list-siteid'),
    path(r'v1/rdr/RDR_Type/<str:rdrtype>/', RDRResource_List.as_view(), name='rdr-list-type'),

    path(r'v1/rdr-xup/', RDRResource_XUP_List.as_view(), name='rdr-xup-list'),
    path(r'v1/rdr-xup/ID/<str:id>/', RDRResource_XUP_Detail.as_view(), name='rdr-xup-detail'),
    path(r'v1/rdr-xup/ResourceID/<str:resourceid>/', RDRResource_XUP_List.as_view(), name='rdr-xup-list-resourceid'),

    path(r'v2/rdr-xup/', RDRResource_XUP_v2_List.as_view(), name='rdr-xup-list-v2'),
    path(r'v3/rdr-xup/', RDRResource_XUP_v3_List.as_view(), name='rdr-xup-list-v3'),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html', 'xml'])
