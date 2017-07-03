from django.conf.urls import include, url
from monitoring_db_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^testresult/$',TestResult_DbList.as_view(),name='testresult-dblist'),
    url(r'^testresult/inca/$', TestResult_DbDetail_Source.as_view(), name='testresult-dblist'),
    url(r'^testresult/nagios/$', TestResult_DbDetail_Source.as_view(), name='testresult-dblist'),
    url(r'^testresult/ID/(?P<pk>[^/]+)/$',TestResult_DbDetail.as_view(),name='testresult-detail'),
]
