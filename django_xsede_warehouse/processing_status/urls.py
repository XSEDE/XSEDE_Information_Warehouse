from django.urls import include, path
from processing_status.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'record/', ProcessingRecord_DbList.as_view(), name='processingrecord-dblist'),
    path(r'record/about/<str:about>/', ProcessingRecord_DbList.as_view(), name='processingrecord-dblist-byabout'),
    path(r'record/resourceid/<str:about>/', ProcessingRecord_DbList.as_view(), name='processingrecord-dblist-byabout'),
    path(r'record/topic/<str:topic>/', ProcessingRecord_DbList.as_view(), name='processingrecord-dblist-bytopic'),
    path(r'record/id/<str:id>/', ProcessingRecord_Detail.as_view(), name='processingrecord-detail'),
    path(r'record/latest/about/<str:about>/', ProcessingRecord_LatestList.as_view(), name='processingrecord-latestlist-byabout'),
    path(r'record/latest/resourceid/<str:about>/', ProcessingRecord_LatestList.as_view(), name='processingrecord-latestlist-byresourceid'),
    path(r'record/latest/topic/<str:topic>/', ProcessingRecord_LatestList.as_view(), name='processingrecord-latestlist-bytopic'),
    path(r'publisherinfo/', PublisherInfo_DbList.as_view(), name='publisherinfo-dblist'),
    path(r'publisherinfo/id/<str:id>/', PublisherInfo_Detail.as_view(), name='publisherinfo-detail'),
    path(r'publisherinfo/resourceid/<str:resourceid>/', PublisherInfo_DbList.as_view(), name='publisherinfo-dblist-byresourceid'),
]
