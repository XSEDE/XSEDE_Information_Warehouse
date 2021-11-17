from django.urls import include, path
from xdcdb.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'xdcdb/ID/<str:id>/', XSEDEResource_Detail.as_view(), name='xdcdb-resource-detail'),
    path(r'xdcdb-pub/ID/<str:id>/', XSEDEResourcePublished_Detail.as_view(), name='xdcdb-resource-pub'),
    path(r'xdcdb/', XSEDEResource_List.as_view(), name='xdcdb-resource-list'),
    path(r'resource/', XSEDEResource_List.as_view(), name='xdcdb-resource-list'),
    path(r'resource/ID/<str:id>/', XSEDEResource_Detail.as_view(), name='xdcdb-resource-detail'),
    path(r'resource-pub/ID/<str:id>/', XSEDEResourcePublished_Detail.as_view(), name='xdcdb-resource-pub'),
    path(r'person/id/<str:id>/', XSEDEPerson_Detail.as_view(), name='xsede-person-detail'),
    path(r'person/portalid/<str:portalid>/', XSEDEPerson_Detail.as_view(), name='xsede-portalid-detail'),
    path(r'person/search_strings/<str:search_strings>/', XSEDEPerson_Search.as_view(), name='xdcdb-person-search'),
    path(r'fos/', XSEDEFos_List.as_view(), name='xdcdb-fos-list'),
    path(r'fos/ID/<str:id>/', XSEDEFos_Detail.as_view(), name='xdcdb-fos-detail'),
    path(r'fos/children/<str:parentid>/', XSEDEFos_List.as_view(), name='xdcdb-fos-children'),
]
