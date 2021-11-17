from django.urls import include, path
from debug.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'dump.html', Debug_Detail.as_view(), name='debug-detail')
]
