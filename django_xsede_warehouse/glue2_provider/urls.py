from django.conf.urls import include, url
from glue2_provider.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^process/doctype/(?P<doctype>[^/]+)/resourceid/(?P<resourceid>[^/]+)/$',
        Glue2ProcessDoc.as_view(),
        name='glue2-process-doc'),
]
