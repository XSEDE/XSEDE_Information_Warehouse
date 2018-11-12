from django.contrib import admin
from processing_status.models import *

# Register your models here.

class ProcessingRecordAdmin(admin.ModelAdmin):
    list_display = ('Topic', 'About', 'ProcessingStart', 'ID')
    list_display_links = ['ID']

class ProcessingErrorAdmin(admin.ModelAdmin):
    list_display = ('Topic', 'About', 'ErrorTime', 'ID')
    list_display_links = ['ID']

class PublisherInfoAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Type', 'Hostname', 'ID')
    list_display_links = ['ID']

# Register your models here.
admin.site.register(ProcessingRecord, ProcessingRecordAdmin)
admin.site.register(ProcessingError, ProcessingErrorAdmin)
admin.site.register(PublisherInfo, PublisherInfoAdmin)
