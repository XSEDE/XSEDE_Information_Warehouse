from django.conf.urls import include, url
from xdcdb.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^xdcdb/$', XSEDEResource_List.as_view(), name='xdcdb-resource-list'),
    url(r'^xdcdb/ID/(?P<id>[^/]+)/$', XSEDEResource_Detail.as_view(), name='xdcdb-resource-detail'),
    url(r'^xdcdb-pub/ID/(?P<id>[^/]+)/$', XSEDEResourcePublished_Detail.as_view(), name='xdcdb-resource-pub'),
    url(r'^resource/$', XSEDEResource_List.as_view(), name='xdcdb-resource-list'),
    url(r'^resource/ID/(?P<id>[^/]+)/$', XSEDEResource_Detail.as_view(), name='xdcdb-resource-detail'),
    url(r'^resource-pub/ID/(?P<id>[^/]+)/$', XSEDEResourcePublished_Detail.as_view(), name='xdcdb-resource-pub'),
    url(r'^person/id/(?P<id>[^/]+)/?$', XSEDEPerson_Detail.as_view(), name='xsede-person-detail'),
    url(r'^person/portalid/(?P<portalid>[^/]+)/?$', XSEDEPerson_Detail.as_view(), name='xsede-portalid-detail'),
    url(r'^person/search_strings/(?P<search_strings>[^/]+)/?$', XSEDEPerson_Search.as_view(), name='xdcdb-person-search'),
    url(r'^fos/$', XSEDEFos_List.as_view(), name='xdcdb-fos-list'),
    url(r'^fos/ID/(?P<id>[^/]+)/$', XSEDEFos_Detail.as_view(), name='xdcdb-fos-detail'),
    url(r'^fos/children/(?P<parentid>[^/]+)/$', XSEDEFos_List.as_view(), name='xdcdb-fos-children'),
]
