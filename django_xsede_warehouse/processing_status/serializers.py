from rest_framework import serializers
from processing_status.models import *
from django.utils.encoding import uri_to_iri
from django.core.urlresolvers import reverse, get_script_prefix
import copy

class ProcessingRecord_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingRecord
        fields = copy.copy([f.name for f in ProcessingRecord._meta.get_fields(include_parents=False)])

class ProcessingRecord_DetailURL_DbSerializer(serializers.ModelSerializer):
    ProcessingStart = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S %Z')
    ProcessingEnd = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S %Z')
    DetailURL = serializers.SerializerMethodField()

    def get_DetailURL(self, ProcessingRecord):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('processingrecord-detail', args=[ProcessingRecord.ID])))
        else:
            return ''
    class Meta:
        model = ProcessingRecord
        fields = copy.copy([f.name for f in ProcessingRecord._meta.get_fields(include_parents=False)])
        fields.append('DetailURL')
