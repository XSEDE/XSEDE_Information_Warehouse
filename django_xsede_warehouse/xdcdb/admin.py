from django.contrib import admin
from xdcdb.models import *

class TGResourceAdmin(admin.ModelAdmin):
    #list_display = ('ResourceID', 'ResourceName', 'SiteID', 'ResourceKits')
    list_display = ('ResourceID', 'SiteID')
    list_display_links = ['ResourceID']
    ordering = ['ResourceID', 'SiteID']

# Register your models here.
admin.site.register(TGResource, TGResourceAdmin)
