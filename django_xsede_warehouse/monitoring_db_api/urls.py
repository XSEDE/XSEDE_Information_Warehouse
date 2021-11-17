from django.urls import include, path
from monitoring_db_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'testresult/',TestResult_DbList.as_view(),name='testresult-dblist'),
    path(r'testresult/inca/', TestResult_DbDetail_Source.as_view(), name='testresult-dblist'),
    path(r'testresult/nagios/', TestResult_DbDetail_Source.as_view(), name='testresult-dblist'),
    path(r'testresult/ID/<str:pk>/',TestResult_DbDetail.as_view(),name='testresult-detail'),
]
