from django.urls import include, path
from speedpage.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'speedpage/', speedpage_List.as_view(), name='speedpage-list'),
    path(r'speedpage/sourceid/<str:sourceid>/destid/<str:destid>/', speedpage_Detail.as_view(), name='speedpage-sourcedest'),
    path(r'speedpage/sourceid/<str:sourceid>/', speedpage_Detail.as_view(), name='speedpage-sourceid'),
    path(r'speedpage/destid/<str:destid>/', speedpage_Detail.as_view(), name='speedpage-destid'),
]
