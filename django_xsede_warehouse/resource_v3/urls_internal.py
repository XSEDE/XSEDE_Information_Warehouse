from django.conf.urls import include, url
from .views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
# Special reg for resource/id/<id> in case there are slashes in the 'id'
urlpatterns = [
    url(r'^relations_cache/?$',
        Relations_Cache.as_view(), name='relations-cache'),
]
