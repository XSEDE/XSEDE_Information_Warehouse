from django.conf.urls import include, url
from resource_status_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
#    url(r'^outages/$',
#        Outages_List.as_view(),
#        name='outages-list'),
#    url(r'^outages/ResourceID/(?P<resourceid>[^/]+)/$',
#        Outages_Detail.as_view(),
#        name='outage-detail'),
#    url(r'^outages/ID/(?P<outageid>[^/]+)/$',
#        Outage_Detail.as_view(),
#        name='outage-detail'),

#    url(r'^monitoring/$',
#        Monitoring_List.as_view(),
#        name='monitoring-list'),
#    url(r'^monitoring/ResourceID/(?P<resourceid>[^/]+)/$',
#        Monitoring_Detail.as_view(),
#        name='monitoring-detail'),
#    url(r'^monitoring/TestID/(?P<testid>[^/]+)/$',
#        Monitoring_Detail.as_view(),
#        name='monitoring-detail'),
    # These are XSEDE allocated resource status for the XUP
    url(r'^status/$',
        Resource_Status_Detail.as_view(),
        name='resource-status-detail'),
    url(r'^status/resourceid/(?P<resourceid>[^/]+)/$',
        Resource_Status_Detail.as_view(),
        name='resource-status-detail'),
   # These are all XSEDE federate resource operational status for the XCSR
    url(r'^ops-status/$',
       Resource_Ops_Status_Detail.as_view(),
       name='resource-ops-status-detail'),
    url(r'^ops-status/resourceid/(?P<resourceid>[^/]+)/$',
       Resource_Ops_Status_Detail.as_view(),
       name='resource-ops-status-detail'),
   # These are all XSEDE federate resource batch statuses
    url(r'^batch-status/$',
       Resource_Batch_Status_Detail.as_view(),
       name='resource-batch-status-detail'),
    url(r'^batch-status/resourceid/(?P<resourceid>[^/]+)/$',
       Resource_Batch_Status_Detail.as_view(),
       name='resource-batch-status-detail'),

#    url(r'^status/active/$',
#        Resource_Status_Detail.as_view(),
#        name='resource-status-detail'),
]
