from django.contrib import admin
from resource_cat.models import *

# Register your models here.
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('Affiliation', 'Name', 'Type', 'ID', 'CreationTime', 'LocalID')
    list_display_links = ['ID']

class ResourceProviderAdmin(admin.ModelAdmin):
    list_display = ('Affiliation', 'Name', 'ID', 'CreationTime', 'LocalID')
    list_display_links = ['ID']

# Register your models here.
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceProvider, ResourceProviderAdmin)
