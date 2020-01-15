from django.contrib import admin
from xdcdb.models import *

class XSEDEResourceAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'SiteID')
    list_display_links = ['ResourceID']
    ordering = ['ResourceID', 'SiteID']

class XSEDELocalUsermapAdmin(admin.ModelAdmin):
    list_display = ('portal_login', 'resource_id', 'local_username', 'ResourceID', 'ID')
    list_display_links = ['ID']
    ordering = ['portal_login', 'resource_id', 'local_username']

class XSEDEPersonAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'portal_login', 'last_name', 'first_name', 'middle_name', 'emails')
    list_display_links = ['person_id']
    ordering = ['portal_login', 'last_name', 'first_name']

# Register your models here.
admin.site.register(TGResource, XSEDEResourceAdmin)
admin.site.register(XSEDELocalUsermap, XSEDELocalUsermapAdmin)
admin.site.register(XSEDEPerson, XSEDEPersonAdmin)
