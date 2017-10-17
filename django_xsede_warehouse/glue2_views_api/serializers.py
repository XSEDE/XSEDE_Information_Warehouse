from rest_framework import serializers
#from drf_toolbox import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from glue2_db.models import ApplicationEnvironment, ApplicationHandle, AbstractService, Endpoint
from glue2_db.serializers import ApplicationHandle_DbSerializer, AbstractService_DbSerializer, Endpoint_DbSerializer

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
