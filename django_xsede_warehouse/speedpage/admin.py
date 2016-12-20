from django.contrib import admin
from speedpage.models import *

class speedpageAdmin(admin.ModelAdmin):
    list_display = ('tstamp', 'sourceid', 'source', 'src_url', 'destid', 'dest', 'dest_url', 'xfer_rate')
    list_display_links = ['sourceid']
    ordering = ['sourceid', 'destid']

# Register your models here.
admin.site.register(speedpage, speedpageAdmin)
