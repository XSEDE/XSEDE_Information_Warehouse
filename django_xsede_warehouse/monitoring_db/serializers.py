from monitoring_db.models import *
from rest_framework import serializers

class TestResult_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON', \
                  'Source', 'Result', 'ErrorMessage')