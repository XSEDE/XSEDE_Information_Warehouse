from django.contrib import admin
from glue2_db.models import *

class AdminDomainAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class UserDomainAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class AccessPolicyAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ContactAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class LocationAdmin (admin.ModelAdmin):
    list_display = ('Name', 'ID', 'CreationTime')
    list_display_links = ['ID']
#
class ApplicationEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ApplicationHandleAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class AbstractServiceAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ServiceType', 'ID', 'CreationTime')
    list_display_links = ['ID']

class EndpointAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'AbstractService', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ComputingManagerAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ExecutionEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ComputingShareAdmin (admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ComputingQueueAdmin (admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ComputingActivityAdmin (admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']
#
class ComputingManagerAcceleratorInfoAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class ComputingShareAcceleratorInfoAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

class AcceleratorEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'Type', 'ID', 'CreationTime')
    list_display_links = ['ID']
#
class EntityHistoryAdmin(admin.ModelAdmin):
    list_display = ('ID', 'DocumentType', 'ResourceID', 'ReceivedTime')
    list_display_links = ['ID']
    readonly_fields = ['ID']

# Register your models here.
admin.site.register(AdminDomain, AdminDomainAdmin)
admin.site.register(UserDomain, UserDomainAdmin)
admin.site.register(AccessPolicy, AccessPolicyAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(ApplicationEnvironment, ApplicationEnvironmentAdmin)
admin.site.register(ApplicationHandle, ApplicationHandleAdmin)
admin.site.register(AbstractService, AbstractServiceAdmin)
admin.site.register(Endpoint, EndpointAdmin)
admin.site.register(ComputingManager, ComputingManagerAdmin)
admin.site.register(ExecutionEnvironment, ExecutionEnvironmentAdmin)
admin.site.register(ComputingShare, ComputingShareAdmin)
admin.site.register(ComputingQueue, ComputingQueueAdmin)
admin.site.register(ComputingActivity, ComputingActivityAdmin)
admin.site.register(ComputingManagerAcceleratorInfo, ComputingManagerAcceleratorInfoAdmin)
admin.site.register(ComputingShareAcceleratorInfo, ComputingShareAcceleratorInfoAdmin)
admin.site.register(AcceleratorEnvironment, AcceleratorEnvironmentAdmin)
admin.site.register(EntityHistory, EntityHistoryAdmin)
