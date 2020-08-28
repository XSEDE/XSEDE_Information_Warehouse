from django.contrib import admin
from projectresources.models import *

class ProjectResourceAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'project_number')
    list_display_links = ['ResourceID']
    ordering = ['ResourceID', 'project_number']
    search_fields = ['ResourceID__iexact', 'project_number__iexact']

# Register your models here.
admin.site.register(ProjectResource, ProjectResourceAdmin)
