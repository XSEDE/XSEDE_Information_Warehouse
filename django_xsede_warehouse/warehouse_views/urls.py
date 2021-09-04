from django.conf.urls import include, url
from warehouse_views.views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^v1/resources/$', RDR_List.as_view(), name='rdr-list'),
    url(r'^v1/resources/SiteID/(?P<info_siteid>[^/]+)/$', RDR_List.as_view(), name='resource-siteID-list'),
    url(r'^v1/resources-active/$', RDR_List_Active.as_view(), name='rdr-list-active'),
    url(r'^v1/resources-xdcdb-active/$', Resource_List_XDCDB_Active.as_view(), name='resource-list-active-xdcdb'),
    url(r'^v1/resources-csa/$', Resource_List_CSA_Active.as_view(), name='resource-list-active-csa'),
    url(r'^v1/resources-sgci/v1.0.0/$', Resource_List_SGCI_Active_100.as_view(), name='resource-list-active-sgci-100'),
    url(r'^v1/resource/ResourceID/(?P<resourceid>[^/]+)/$', RDR_Detail.as_view(), name='rdr-detail-resourceid'),
    url(r'^v1/resource/RdrID/(?P<rdrid>[^/]+)/$', RDR_Detail.as_view(), name='rdr-detail-rdrid'),
    url(r'^v1/software/$', Software_Full.as_view(), name='software-list'),
    url(r'^v1/software/ID/(?P<id>[^/]+)/$', Software_Full.as_view(), name='software-detail'),
    url(r'^v1/software/ResourceID/(?P<resourceid>[^/]+)/$', Software_Full.as_view(), name='software-detail'),
    url(r'^v1/software/AppName/(?P<appname>[^/]+)/$', Software_Full.as_view(), name='software-detail'),
    url(r'^v1/software-xup/$', Software_XUP_v1_List.as_view(), name='software-xup-list'),
    url(r'^v1/community-software-xup/$', Community_Software_XUP_v1_List.as_view(), name='community-software-xup-list'),
    # 120 minutes
    url(r'^v1/software-cached/$', cache_page(60 * 120)(Software_Full.as_view()), name='software-cache-list'),
]
