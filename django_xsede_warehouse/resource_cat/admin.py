from django.contrib import admin
from resource_cat.models import *

# Register your models here.
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('Affiliation', 'LocalID', 'Name', 'Type', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ResourceProviderAdmin(admin.ModelAdmin):
    list_display = ('Affiliation', 'ID', 'LocalID', 'Name', 'CreationTime')
    list_display_links = ['ID']

# Register your models here.
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceProvider, ResourceProviderAdmin)
