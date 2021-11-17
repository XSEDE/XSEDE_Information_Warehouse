from django.urls import include, path
from warehouse_views.views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'v1/resources/', RDR_List.as_view(), name='rdr-list'),
    path(r'v1/resources/SiteID/<str:info_siteid>/', RDR_List.as_view(), name='resource-siteID-list'),
    path(r'v1/resources-active/', RDR_List_Active.as_view(), name='rdr-list-active'),
    path(r'v1/resources-xdcdb-active/', Resource_List_XDCDB_Active.as_view(), name='resource-list-active-xdcdb'),
    path(r'v1/resources-csa/', Resource_List_CSA_Active.as_view(), name='resource-list-active-csa'),
    path(r'v1/resources-sgci/v1.0.0/', Resource_List_SGCI_Active_100.as_view(), name='resource-list-active-sgci-100'),
    path(r'v1/resource/ResourceID/<str:resourceid>/', RDR_Detail.as_view(), name='rdr-detail-resourceid'),
    path(r'v1/resource/RdrID/<str:rdrid>/', RDR_Detail.as_view(), name='rdr-detail-rdrid'),
    path(r'v1/software/', Software_Full.as_view(), name='software-list'),
    path(r'v1/software/ID/<str:id>/', Software_Full.as_view(), name='software-detail'),
    path(r'v1/software/ResourceID/<str:resourceid>/', Software_Full.as_view(), name='software-detail'),
    path(r'v1/software/AppName/<str:appname>/', Software_Full.as_view(), name='software-detail'),
    path(r'v1/software-xup/', Software_XUP_v1_List.as_view(), name='software-xup-list'),
    path(r'v1/community-software-xup/', Community_Software_XUP_v1_List.as_view(), name='community-software-xup-list'),
    # 120 minutes
    path(r'v1/software-cached/', cache_page(60 * 120)(Software_Full.as_view()), name='software-cache-list'),
]
