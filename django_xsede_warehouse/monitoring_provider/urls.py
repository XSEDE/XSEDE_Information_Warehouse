from django.urls import include, path
from monitoring_provider.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'process/doctype/<str:doctype>/resourceid/<str:resourceid>/',
        Glue2ProcessDoc.as_view(),
        name='glue2-process-doc'),
]
