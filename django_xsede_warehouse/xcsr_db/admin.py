from django.contrib import admin
from xcsr_db.models import *

class ComponentSPRequirementAdmin(admin.ModelAdmin):
    list_display = ('ComponentName', 'SPClass', 'Requirement')
    list_display_links = ['ComponentName', 'SPClass']
    readonly_fields = ['UpdateTime', 'UpdateUser']

    def save_model(self, request, obj, form, change):
        obj.UpdateUser = request.user.username
        obj.save()

# Register your models here.
admin.site.register(ComponentSPRequirement, ComponentSPRequirementAdmin)