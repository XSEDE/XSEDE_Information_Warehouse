from django.conf.urls import include, url
from debug.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^dump.html$',
        Debug_Detail.as_view(),
        name='debug-detail')
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
