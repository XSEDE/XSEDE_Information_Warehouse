from glue2_db.models import *
from rest_framework import serializers

class AdminDomain_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDomain
        fields = ('ID', 'Name', 'CreationTime', 'Validity' , 'EntityJSON', \
                  'Description', 'WWW', 'Distributed', 'Owner')

class UserDomain_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDomain
        fields = ('ID', 'Name', 'CreationTime', 'Validity' , 'EntityJSON', \
                  'Description', 'WWW', 'Level', 'UserManager', 'Member')

class AccessPolicy_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessPolicy
        fields = ('ID', 'Name', 'CreationTime', 'Validity' , 'EntityJSON', \
                  'Scheme', 'Rule')

class Contact_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('ID', 'Name', 'CreationTime', 'Validity' , 'EntityJSON', \
                  'Detail', 'Type')

class Location_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('ID', 'Name', 'CreationTime', 'Validity' , 'EntityJSON')
#
class ApplicationEnvironment_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationEnvironment
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON', \
                  'Description', 'AppName', 'AppVersion')

class ApplicationHandle_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationHandle
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON', \
                  'ApplicationEnvironment', 'Type', 'Value')

class AbstractService_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractService
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON', \
                  'ServiceType', 'Type', 'QualityLevel')

class Endpoint_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON', \
                  'AbstractService', 'HealthState', 'ServingState', 'URL', \
                  'QualityLevel', 'InterfaceVersion', 'InterfaceName')

class ComputingManager_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingManager
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON')

class ExecutionEnvironment_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionEnvironment
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON')

class ComputingShare_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingShare
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON')

class ComputingQueue_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingQueue
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON')

class ComputingActivity_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingActivity
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON')

class ComputingManagerAcceleratorInfo_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingManagerAcceleratorInfo
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON')

class ComputingManagerAcceleratorInfo_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingManagerAcceleratorInfo
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON')

class ComputingShareAcceleratorInfo_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputingShareAcceleratorInfo
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON')

class AcceleratorEnvironment_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceleratorEnvironment
        fields = ('ID', 'ResourceID', 'Name', 'CreationTime', 'Validity', 'EntityJSON', \
                  'Type')

class EntityHistory_DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityHistory
        fields = ('ID', 'DocumentType', 'ResourceID', 'ReceivedTime', 'EntityJSON')

class EntityHistory_Usage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EntityHistory
        fields = ('DocumentType', 'ResourceID', 'ReceivedTime')
