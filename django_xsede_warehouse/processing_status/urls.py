from django.conf.urls import include, url
from processing_status.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^record/$', ProcessingRecord_DbList.as_view(), name='processingrecord-dblist'),
    url(r'^record/about/(?P<about>[^/]+)/$', ProcessingRecord_DbList.as_view(), name='processingrecord-dblist-byabout'),
    url(r'^record/resourceid/(?P<about>[^/]+)/$', ProcessingRecord_DbList.as_view(), name='processingrecord-dblist-byabout'),
    url(r'^record/topic/(?P<topic>[^/]+)/$', ProcessingRecord_DbList.as_view(), name='processingrecord-dblist-bytopic'),
    url(r'^record/id/(?P<id>[^/]+)/$', ProcessingRecord_Detail.as_view(), name='processingrecord-detail'),
    url(r'^record/latest/(about|resourceid)/(?P<about>[^/]+)/$', ProcessingRecord_LatestList.as_view(), name='processingrecord-latestlist-byabout'),
    url(r'^record/latest/topic/(?P<topic>[^/]+)/$', ProcessingRecord_LatestList.as_view(), name='processingrecord-latestlist-bytopic'),
    url(r'^publisherinfo/$', PublisherInfo_DbList.as_view(), name='publisherinfo-dblist'),
    url(r'^publisherinfo/id/(?P<id>[^/]+)/$', PublisherInfo_Detail.as_view(), name='publisherinfo-detail'),
    url(r'^publisherinfo/resourceid/(?P<resourceid>[^/]+)/$', PublisherInfo_DbList.as_view(), name='publisherinfo-dblist-byresourceid'),
]
