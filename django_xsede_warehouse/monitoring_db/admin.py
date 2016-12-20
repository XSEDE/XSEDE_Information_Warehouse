from django.contrib import admin
from monitoring_db.models import *

class TestResultAdmin(admin.ModelAdmin):
    list_display = ('ResourceID', 'Name', 'ID', 'CreationTime')
    list_display_links = ['ID']

# Register your models here.
admin.site.register(TestResult, TestResultAdmin)