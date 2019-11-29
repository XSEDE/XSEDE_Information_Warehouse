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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth import views
from django.http import HttpResponse
from . import views
#from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView, RedirectView
from rest_framework_swagger.views import get_swagger_view
from xsede_warehouse.settings import API_BASE

urlpatterns_public = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^allocations/v1/', include('allocations.urls')),
    url(r'^glue2-db-api/v1/', include('glue2_db_api.urls')),
    url(r'^glue2-provider-api/v1/', include('glue2_provider.urls')),
    url(r'^glue2-views-api/v1/', include('glue2_views_api.urls')),
    url(r'^goendpoint-api/v1/', include('goendpoint_api.urls')),
    url(r'^monitoring-db-api/v1/', include('monitoring_db_api.urls')),
    url(r'^monitoring-provider-api/v1/', include('monitoring_provider.urls')),
    url(r'^monitoring-views-api/v1/', include('monitoring_views_api.urls')),
    url(r'^outages/v1/', include('outages.urls')),
    url(r'^processing-status/', include('processing_status.urls')),
    url(r'^projectresources/v1/', include('projectresources.urls')),
    url(r'^rdr-db/', include('rdr_db.urls')),
    url(r'^resource-api/v1/', include('resource_cat.urls')),
    url(r'^resource-api/v2/', include('resource_v2.urls')),
    url(r'^resource-status-api/v1/', include('resource_status_api.urls')),
    url(r'^speedpage/v1/', include('speedpage.urls')),
    url(r'^xcsr-db/v1/', include('xcsr_db.urls')),
    url(r'^xdcdb/v1/', include('xdcdb.urls')),
    url(r'^xdinfo/v1/', include('xdinfo.urls')),
    url(r'^warehouse-views/', include('warehouse_views.urls')),
    url(r'^home/', views.home, name='home'),
    url(r'^', include ('django.contrib.auth.urls')),
    url(r'^', include('social_django.urls', namespace='social'))
]

schema_view = get_swagger_view(title='XSEDE Warehouse API', url=API_BASE, patterns=urlpatterns_public)

urlpatterns_internal = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-docs/', schema_view, name='swagger'),
    url(r'^debug/', include('debug.urls')),
    url(r'^favicon\.ico$', lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="image/ico"), name="/static/favicon.ico"),
    url(r'^robots\.txt$', lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"), name="/static/robots.txt"),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^feedback(\.html)?$',TemplateView.as_view(template_name='feedback.html')),
]

urlpatterns = urlpatterns_internal + urlpatterns_public
