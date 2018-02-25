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
schema_view = get_swagger_view(title='XSEDE Warehouse API')

urlpatterns = [
    url('^$', TemplateView.as_view(template_name='wh.html')),
    url('^admin/', include(admin.site.urls)),
    url('^glue2-db-api/v1/', include('glue2_db_api.urls')),
    url('^glue2-provider-api/v1/', include('glue2_provider.urls')),
    url('^glue2-views-api/v1/', include('glue2_views_api.urls')),
    url('^goendpoint-api/v1/', include('goendpoint_api.urls')),
    url('^monitoring-db-api/v1/', include('monitoring_db_api.urls')),
    url('^monitoring-provider-api/v1/', include('monitoring_provider.urls')),
    url('^monitoring-views-api/v1/', include('monitoring_views_api.urls')),
    url('^outages/v1/', include('outages.urls')),
    url('^processing-status/', include('processing_status.urls')),
    url('^projectresources/v1/', include('projectresources.urls')),
    url('^rdr-db/', include('rdr_db.urls')),
    url('^resource-status-api/v1/', include('resource_status_api.urls')),
    url('^speedpage/v1/', include('speedpage.urls')),
    url('^xcsr-db/v1/', include('xcsr_db.urls')),
    url('^xdcdb/v1/', include('xdcdb.urls')),
    url('^xdinfo/v1/', include('xdinfo.urls')),
    url('^warehouse-views/', include('warehouse_views.urls')),
    url('^api-docs/', schema_view, name='swagger')
]
