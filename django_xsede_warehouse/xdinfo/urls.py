from django.conf.urls import patterns, include, url
from xdinfo.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
#    url(r'^xdinfo/cli/$',
#        xdinfo_List.as_view(),
#        name='xdinfo-help'),
#    url(r'^xdinfo/cli/(?P<infotype>[^/]+)/$',
#        xdinfo_Cmd.as_view(),
#        name='xdinfo-detail'),
    url(r'^(?P<infoformat>[^/]+)/xdinfo/cli/?$',
        xdinfo_Cmd.as_view(),
        name='xdinfo-xtraargs'),
    url(r'^(?P<infoformat>[^/]+)/xdinfo/cli/(?P<infotype>[^/]+)/?$',
        xdinfo_Cmd.as_view(),
        name='xdinfo-xtraargs'),
#    url(r'^xdinfo/cli/(?P<infotype>[^/]+)/(?P<slug>.+)/$',
#        xdinfo_Cmd.as_view(),
#        name='xdinfo-xtraargs'),
    url(r'^(?P<infoformat>[^/]+)/xdinfo/cli/(?P<infotype>[^/]+)/(?P<slug>.+)/?$',
        xdinfo_Cmd.as_view(),
        name='xdinfo-xtraargs'),
    #url(r'^xdinfo/cli/(?P<infotype>[^/]+)/(?P<arg1>[^/]+)/$',
    #    xdinfo_Cmd.as_view(),
    #    name='xdinfo-xtraargs'),
    #url(r'^xdinfo/cli/(?P<infotype>[^/]+)/at/(?P<arg1>[^/]+)/$',
    #    xdinfo_Cmd.as_view(),
    #    name='xdinfo-xtraargsat'),
    #url(r'^xdinfo/cli/(?P<infotype>[^/]+)/on/(?P<arg1>[^/]+)/$',
    #    xdinfo_Cmd.as_view(),
    #    name='xdinfo-xtraargson'),
    #url(r'^xdinfo/cli/(?P<infotype>[^/]+)/(?P<arg1>[^/]+)/(?P<arg2>[^/]+)/$',
    #    xdinfo_Cmd.as_view(),
    #    name='xdinfo-xtraargson'),

#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
