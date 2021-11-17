from django.urls import include, path
from resource_status_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    # These are XSEDE allocated resource status for the XUP
    path(r'status/',
        Resource_Status_Detail.as_view(),
        name='resource-status-detail'),
    path(r'status/resourceid/<str:resourceid>/',
        Resource_Status_Detail.as_view(),
        name='resource-status-detail'),
   # These are all XSEDE federate resource operational status for the XCSR
    path(r'ops-status/',
       Resource_Ops_Status_Detail.as_view(),
       name='resource-ops-status-detail'),
    path(r'ops-status/resourceid/<str:resourceid>/',
       Resource_Ops_Status_Detail.as_view(),
       name='resource-ops-status-detail'),
   # These are all XSEDE federate resource batch statuses
    path(r'batch-status/',
       Resource_Batch_Status_Detail.as_view(),
       name='resource-batch-status-detail'),
    path(r'batch-status/resourceid/<str:resourceid>/',
       Resource_Batch_Status_Detail.as_view(),
       name='resource-batch-status-detail'),
]
