from django.contrib import admin
from xdcdb.models import *

class XcdbResourceAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'SiteID')
    list_display_links = ['ResourceID']
    ordering = ['ResourceID', 'SiteID']

class XSEDELocalUsermapAdmin(admin.ModelAdmin):
    list_display = ('portal_login', 'resource_id', 'local_username', 'ResourceID', 'ID')
    list_display_links = ['ID']
    ordering = ['portal_login', 'resource_id', 'local_username']

# Register your models here.
admin.site.register(TGResource, XcdbResourceAdmin)
admin.site.register(XSEDELocalUsermap, XSEDELocalUsermapAdmin)
