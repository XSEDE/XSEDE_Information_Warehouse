from rest_framework import serializers
#from drf_toolbox import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from glue2_db.models import ApplicationEnvironment, ApplicationHandle, AbstractService, ComputingActivity, ComputingQueue, Endpoint
from glue2_db.serializers import ApplicationHandle_DbSerializer, AbstractService_DbSerializer, Endpoint_DbSerializer
from django.urls import reverse, get_script_prefix
from django.utils.encoding import uri_to_iri
import copy

class ApplicationEnvironment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationEnvironment
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime',
                  'Description', 'AppName', 'AppVersion')

class ApplicationHandle_Serializer(serializers.ModelSerializer):
#    ApplicationEnvironment = ApplicationEnvironment_Serializer(read_only=True, required=False)
    AppName = serializers.CharField(source='ApplicationEnvironment.AppName')
    AppVersion = serializers.CharField(source='ApplicationEnvironment.AppVersion')
    Description = serializers.CharField(source='ApplicationEnvironment.Description')
    class Meta:
        model = ApplicationHandle
        fields = ('ResourceID', 'AppName', 'AppVersion', 'Description',
                  'Type', 'Value',
                  'CreationTime','ID')
#                  'Name', 'ApplicationEnvironment')

class AbstractService_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractService
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime',
                  'ServiceType', 'Type', 'QualityLevel')

class EndpointServices_Serializer(serializers.ModelSerializer):
#    AbstractService = AbstractService_Serializer(read_only=True, required=False)
    ServiceType = serializers.CharField(source='AbstractService.ServiceType')
    class Meta:
        model = Endpoint
        fields = ('ResourceID', 'InterfaceName', 'InterfaceVersion', 'URL',
                  'QualityLevel', 'ServingState', 'HealthState', 'ServiceType',
                  'CreationTime', 'ID')
#                  'Name', 'AbstractService')

class ComputingActivity_Expand_Serializer(serializers.ModelSerializer):
    DetailURL = serializers.SerializerMethodField()
    StandardState = serializers.SerializerMethodField()
    def get_DetailURL(self, ComputingActivity):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('jobs-detail', args=[ComputingActivity.ID])))
        else:
            return ''
    def get_StandardState(self, ComputingActivity):
        for s in ComputingActivity.EntityJSON.get('State'):
            if s.startswith('ipf:'):
                return s[4:]
        return ''
    class Meta:
        model = ComputingActivity
        fields = copy.copy([f.name for f in ComputingActivity._meta.get_fields(include_parents=False)])
        fields.append('DetailURL')
        fields.append('StandardState')

class ComputingQueue_Expand_Serializer(serializers.ModelSerializer):
    JobQueue = serializers.SerializerMethodField()
    def get_JobQueue(self, ComputingQueue):
#        try:
#            sort_by = self.context.get('sort_by', None)
#            if sort_by:
#                jobsort = {}
#                for key in ComputingQueue.EntityJSON:
#                    jobin = ComputingQueue.EntityJSON[key]
#                    try:
#                        if sort_by in ('RequestedTotalWallTime', 'RequestedSlots'):
#                            prefix = '{:d030d}'.format(jobin[sort_by])
#                        elif sort_by in ('SubmissionTime', 'StartTime'):
#                            prefix = '{:%Y/%m/%d %H:%M:%S %Z}'.format(jobin[sort_by])
#                        else:
#                            prefix = jobin[sort_by]
#                    except:
#                        prefix = jobin[sort_by]
#                    jobsort[prefix + ':' + jobin['ID']] = jobin
#            else:
#                jobsort = ComputingQueue.EntityJSON
#        except Exception as e:
#            jobsort = ComputingQueue.EntityJSON
        response = []
#        for key in sorted(jobsort):
        for key in ComputingQueue.EntityJSON:
            jobin = ComputingQueue.EntityJSON[key]
            jobout = {'ID': jobin['LocalIDFromManager']}
            for s in jobin['State']:
                if s.startswith('ipf:'):
                    jobout['State'] = s[4:]
            jobout['Name'] = jobin['Name']
            jobout['LocalOwner'] = jobin['LocalOwner']
            jobout['Queue'] = jobin['Queue']
            jobout['SubmissionTime'] = jobin['SubmissionTime']
            jobout['RequestedSlots'] = jobin['RequestedSlots']
            jobout['RequestedTotalWallTime'] = jobin['RequestedTotalWallTime']
            jobout['StartTime'] = jobin.get('StartTime', None)
            response.append(jobout)
        return response
    class Meta:
        model = ComputingQueue
        fields = ('ResourceID', 'Name', 'CreationTime', 'Validity', 'ID', 'JobQueue')
