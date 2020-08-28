from django.contrib import admin
from monitoring_db.models import *

class TestResultAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'Result', 'ID', 'CreationTime')
    list_display_links = ['ID']
    search_fields = ['Name', 'ResourceID__iexact', 'ID__startswith']

# Register your models here.
admin.site.register(TestResult, TestResultAdmin)
