from rest_framework import serializers
from monitoring_db.models import TestResult
from django.utils.encoding import uri_to_iri
from django.core.urlresolvers import reverse, get_script_prefix

class TestResult_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime',
                  'Source', 'Result', 'ErrorMessage',
                  'IsSoftware', 'IsService', 'EntityJSON')

class TestResult_DetailURL_Serializer(serializers.ModelSerializer):
    CreationTime = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S %Z')
    DetailURL = serializers.SerializerMethodField()
    
    def get_DetailURL(self, TestResult):
        http_request = self.context.get('request')
        url_name = self.context.get('detail_url_name')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse(url_name, args=[TestResult.ID])))
        else:
            return ''

    class Meta:
        model = TestResult
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime',
                  'Source', 'Result', 'ErrorMessage',
                  'IsSoftware', 'IsService', 'EntityJSON', 'DetailURL')
