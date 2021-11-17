from django.urls import include, path
from glue2_db_api.views import *
from goendpoint_api.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'goservices/', goServices_List.as_view(), name='goservices-list'),
    path(r'goservices/ID/<str:id>/', goServices_Detail.as_view(), name='goservices-detail'),
    path(r'goservices/ResourceID/<str:resourceid>/', goServices_Detail.as_view(), name='goservices-detail'),
    path(r'goservices/InterfaceName/<str:interfacename>/', goServices_Detail.as_view(), name='goservices-detail'),
    path(r'goservices/ServiceType/<str:servicetype>/', goServices_Detail.as_view(), name='goservices-detail'),
]
