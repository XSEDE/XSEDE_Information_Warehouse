from django.contrib import admin
from outages.models import *

class OutagesAdmin(admin.ModelAdmin):
#OutageID,ResourceID,WebURL,Subject,Content,OutageStart,OutageEnd,SiteID
    list_display = ('OutageID','ResourceID','WebURL','Subject','Content','OutageStart','OutageEnd','SiteID')
    list_display_links = ['OutageID']
    ordering = ['OutageID', 'ResourceID']
    search_fields = ['Subject', 'ResourceID__iexact', 'OutageID__iexact']

# Register your models here.
admin.site.register(Outages, OutagesAdmin)
