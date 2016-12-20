from django.contrib import admin
from rdr_db.models import *

class RDRResourceAdmin(admin.ModelAdmin):
    list_display = ('rdr_resource_id', 'info_resourceid', 'rdr_type', 'resource_descriptive_name')
    list_display_links = ['rdr_resource_id']
    ordering = ['info_resourceid', 'rdr_type']

# Register your models here.
admin.site.register(RDRResource, RDRResourceAdmin)