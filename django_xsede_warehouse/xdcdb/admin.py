from django.contrib import admin
from xdcdb.models import *

class XSEDEResourceAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'SiteID')
    list_display_links = ['ResourceID']
    ordering = ['ResourceID', 'SiteID']
    search_fields = ['ResourceID__iexact', 'SiteID__iexact']

class XSEDELocalUsermapAdmin(admin.ModelAdmin):
    list_display = ('portal_login', 'resource_id', 'local_username', 'ResourceID', 'ID')
    list_display_links = ['ID']
    ordering = ['portal_login', 'resource_id', 'local_username']
    search_fields = ['portal_login__iexact', 'resource_id__iexact', 'local_username__iexact', 'ResourceID__iexact', 'ID__iexact']

class XSEDEPersonAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'portal_login', 'last_name', 'first_name', 'middle_name', 'emails')
    list_display_links = ['person_id']
    ordering = ['portal_login', 'last_name', 'first_name']
    search_fields = ['person_id__iexact', 'portal_login__iexact', 'last_name', 'first_name', 'emails']

# Register your models here.
admin.site.register(TGResource, XSEDEResourceAdmin)
admin.site.register(XSEDELocalUsermap, XSEDELocalUsermapAdmin)
admin.site.register(XSEDEPerson, XSEDEPersonAdmin)
