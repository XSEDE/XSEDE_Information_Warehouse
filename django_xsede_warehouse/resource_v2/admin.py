from django.contrib import admin
from resource_v2.models import *

# Register your models here.
class ResourceV2Admin(admin.ModelAdmin):
    list_display = ('Affiliation', 'Name', 'Type', 'ID', 'CreationTime', 'LocalID')
    list_display_links = ['ID']

class ResourceV2ProviderAdmin(admin.ModelAdmin):
    list_display = ('Affiliation', 'Name', 'ID', 'CreationTime', 'LocalID')
    list_display_links = ['ID']

class ResourceV2GuideAdmin(admin.ModelAdmin):
    list_display = ('Affiliation', 'Name', 'ID', 'CreationTime', 'LocalID')
    list_display_links = ['ID']

class ResourceV2GuideResourceAdmin(admin.ModelAdmin):
    list_display = ('CuratedGuideID', 'ResourceID', 'ID')
    list_display_links = ['ID']

# Register your models here.
admin.site.register(ResourceV2, ResourceV2Admin)
admin.site.register(ResourceV2Provider, ResourceV2ProviderAdmin)
admin.site.register(ResourceV2Guide, ResourceV2GuideAdmin)
admin.site.register(ResourceV2GuideResource, ResourceV2GuideResourceAdmin)
