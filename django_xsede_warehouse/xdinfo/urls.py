from django.urls import include, path
from django.views.decorators.cache import cache_page
from xdinfo.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'<str:infoformat>/xdinfo/cli/', xdinfo_Cmd.as_view(), name='xdinfo-xtraargs'),
    path(r'<str:infoformat>/xdinfo/cli/<str:infotype>/software', cache_page(60 * 15)(xdinfo_Cmd.as_view()), name='xdinfo-cache-xtraargs'),
    path(r'<str:infoformat>/xdinfo/cli/<str:infotype>/soft', cache_page(60 * 15)(xdinfo_Cmd.as_view()), name='xdinfo-cache-xtraargs'),
    path(r'<str:infoformat>/xdinfo/cli/<str:infotype>/', xdinfo_Cmd.as_view(), name='xdinfo-xtraargs'),
    path(r'<str:infoformat>/xdinfo/cli/<str:infotype>/<str:slug>/', xdinfo_Cmd.as_view(), name='xdinfo-xtraargs'),
]
