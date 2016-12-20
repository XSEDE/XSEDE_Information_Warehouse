from rest_framework import serializers
#from drf_toolbox import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from monitoring_db.models import TestResult

class TestResult_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime',
                  'Source', 'Result', 'ErrorMessage')