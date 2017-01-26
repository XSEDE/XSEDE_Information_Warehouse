from django.conf.urls import patterns, include, url
from processing_status.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^record/$',
        ProcessingRecord_DbList.as_view(),
        name='processingrecord-dblist'),
    url(r'^record/resourceid/(?P<resourceid>[^/]+)/$',
       ProcessingRecord_DbList.as_view(),
       name='processingrecord-dblist'),
    url(r'^record/id/(?P<id>[^/]+)/$',
       ProcessingRecord_Detail.as_view(),
       name='processingrecord-detail'),
]
