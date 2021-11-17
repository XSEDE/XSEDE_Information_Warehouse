"""xsede_warehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import TemplateView, RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from . import views

urlpatterns_public = [
    path(r'allocations/v1/', include('allocations.urls')),
    path(r'glue2-db-api/v1/', include('glue2_db_api.urls')),
    path(r'glue2-provider-api/v1/', include('glue2_provider.urls')),
    path(r'glue2-views-api/v1/', include('glue2_views_api.urls')),
    path(r'goendpoint-api/v1/', include('goendpoint_api.urls')),
    path(r'monitoring-db-api/v1/', include('monitoring_db_api.urls')),
    path(r'monitoring-provider-api/v1/', include('monitoring_provider.urls')),
    path(r'monitoring-views-api/v1/', include('monitoring_views_api.urls')),
    path(r'outages/v1/', include('outages.urls')),
    path(r'processing-status/', include('processing_status.urls')),
    path(r'projectresources/v1/', include('projectresources.urls')),
    path(r'rdr-db/', include('rdr_db.urls')),
#    path(r'resource-api/v1/', include('resource_cat.urls')),
#    path(r'resource-api/v2/', include('resource_v2.urls')),
    path(r'resource-api/v3/', include('resource_v3.urls')),
    path(r'resource-status-api/v1/', include('resource_status_api.urls')),
    path(r'speedpage/v1/', include('speedpage.urls')),
    path(r'xcsr-db/v1/', include('xcsr_db.urls')),
    path(r'xdcdb/v1/', include('xdcdb.urls')),
    path(r'xdinfo/v1/', include('xdinfo.urls')),
    path(r'warehouse-views/', include('warehouse_views.urls')),
    path(r'home/', views.home, name='home'),
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls', namespace='social'))
]

urlpatterns_internal = [
    path(r'admin/', admin.site.urls),
    path(r'api-docs/', RedirectView.as_view(url='/api/schema/swagger-ui/')),
    path(r'api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(r'api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc',),
    path(r'api/schema/swagger-ui/', SpectacularSwaggerView.as_view(template_name='swagger-ui.html', url_name='schema'), name='swagger-ui',),
    path(r'debug/', include('debug.urls')),
    path(r'favicon.ico', lambda x: HttpResponse('User-Agent: *\nDisallow:', content_type='image/ico'), name='/static/favicon.ico'),
    path(r'robots.txt', lambda x: HttpResponse('User-Agent: *\nDisallow:', content_type='text/plain'), name='/static/robots.txt'),
    path(r'', TemplateView.as_view(template_name='index.html')),
    path(r'info/feedback.html',TemplateView.as_view(template_name='feedback.html')),
    path(r'resource-api/v3/', include('resource_v3.urls_internal')),
]

urlpatterns = urlpatterns_internal + urlpatterns_public
