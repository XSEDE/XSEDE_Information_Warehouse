from processing_status.models import *
from rest_framework import serializers

class ProcessingRecord_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingRecord
        fields = ('ID', 'Topic', 'About', \
                  'ProcessingNode', 'ProcessingApplication', 'ProcessingFunction', \
                  'ProcessingStart', 'ProcessingEnd', 'ProcessingCode', 'ProcessingMessage')
