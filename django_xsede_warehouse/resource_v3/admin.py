from django.contrib import admin
from .models import *

# Register your models here.
class ResourceV3Catalog_Admin(admin.ModelAdmin):
    list_display = ('Affiliation', 'Name', 'ID')
    list_display_links = ['ID']
    readonly_fields = ('created_at', 'updated_at')

class ResourceV3Local_Admin(admin.ModelAdmin):
    list_display = ('Affiliation', 'LocalID', 'CreationTime', 'ID')
    list_display_links = ['ID']

class ResourceV3_Admin(admin.ModelAdmin):
    list_display = ('Affiliation', 'Name', 'ResourceGroup', 'Type', 'ID')
    list_display_links = ['ID']

class ResourceV3Relation_Admin(admin.ModelAdmin):
    list_display = ('FirstResourceID', 'SecondResourceID', 'RelationType', 'ID')
    list_display_links = ['ID']

# Register your models here.
admin.site.register(ResourceV3Catalog, ResourceV3Catalog_Admin)
admin.site.register(ResourceV3Local, ResourceV3Local_Admin)
admin.site.register(ResourceV3, ResourceV3_Admin)
admin.site.register(ResourceV3Relation, ResourceV3Relation_Admin)
