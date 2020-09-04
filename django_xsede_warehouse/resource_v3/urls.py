from django.conf.urls import include, url
from .views import *
from django.views.decorators.cache import cache_page

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
# Special reg for resource/id/<id> in case there are slashes in the 'id'
urlpatterns = [
    url(r'^catalog_search/?$',
        Catalog_Search.as_view(), name='catalog-search'),
    url(r'^catalog/id/(?P<id>.+)/$',
        Catalog_Detail.as_view(), name='catalog-detail'),
    url(r'^local/id/(?P<id>.+)/$',
        Local_Detail.as_view(), name='local-detail-globalid'),
    url(r'^local_search/?$',
        Local_Search.as_view(), name='local-search'),
#    url(r'^provider/id/(?P<id>.+)/$',
#        Provider_Detail.as_view(), name='provider-detail'),
#    url(r'^provider_search/?$',
##        cache_page(60 * 60)(Provider_Search.as_view()), name='provider-search'),
#        Provider_Search.as_view(), name='provider-search'),
    url(r'^resource_types/?$',
        cache_page(60 * 60)(Resource_Types_List.as_view()), name='resource-types-list'),
    url(r'^resource/id/(?P<id>.+)/$',
        Resource_Detail.as_view(), name='resource-detail'),
    url(r'^resource_search/?$',
        Resource_Search.as_view(), name='resource-search'),
    url(r'^resource_esearch/?$',
        Resource_ESearch.as_view(), name='resource-esearch'),
    url(r'^event/id/(?P<id>.+)/$',
        Event_Detail.as_view(), name='event-detail'),
    url(r'^event_search/?$',
        cache_page(60 * 5)(Event_Search.as_view()), name='event-search'),
#    url(r'^guide/id/(?P<id>.+)/$',
#        Guide_Detail.as_view(), name='guide-detail'),
#    url(r'^guide_search/?$',
#        Guide_Search.as_view(), name='guide-search'),
]
