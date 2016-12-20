from glue2_db.models import *
from rest_framework import serializers

class ApplicationEnvironment_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationEnvironment
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON', \
                  'Description', 'AppName', 'AppVersion')

class ApplicationHandle_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationHandle
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON', \
                  'ApplicationEnvironment', 'Type', 'Value')

class AbstractService_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractService
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON', \
                  'ServiceType', 'Type', 'QualityLevel')

class Endpoint_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON', \
                  'AbstractService', 'HealthState', 'ServingState', 'URL', \
                  'QualityLevel', 'InterfaceVersion', 'InterfaceName')

class ComputingManager_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingManager
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON')

class ExecutionEnvironment_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionEnvironment
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON')

class Location_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON')

class ComputingShare_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingShare
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON')

class ComputingActivity_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingActivity
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'EntityJSON')

class EntityHistory_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityHistory
        fields = ('ID', 'DocumentType', 'ResourceID', 'ReceivedTime', 'EntityJSON')
