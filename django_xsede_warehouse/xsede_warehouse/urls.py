"""xsede_warehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
#from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView

#from rest_framework_swagger.views import SwaggerResourcesView, SwaggerApiView, SwaggerUIView
from rest_framework_swagger.views import get_swagger_view
from xsede_warehouse.settings import API_BASE
schema_view = get_swagger_view(title='XSEDE Warehouse API', url=API_BASE)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='wh.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^debug/', include('debug.urls', namespace="hidden_apis")),
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
    url(r'^resource-status-api/v1/', include('resource_status_api.urls')),
    url(r'^speedpage/v1/', include('speedpage.urls')),
    url(r'^xcsr-db/v1/', include('xcsr_db.urls')),
    url(r'^xdcdb/v1/', include('xdcdb.urls')),
    url(r'^xdinfo/v1/', include('xdinfo.urls')),
    url(r'^warehouse-views/', include('warehouse_views.urls')),
    url(r'^api-docs/', schema_view, name='swagger')
]
