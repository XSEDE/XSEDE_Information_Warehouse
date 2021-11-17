from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from glue2_db.models import *
from glue2_db.serializers import ApplicationHandle_DbSerializer, AbstractService_DbSerializer, Endpoint_DbSerializer
from rdr_db.models import *

class goEndpointServices_Serializer(serializers.Serializer):
    ID = serializers.CharField()
    URL = serializers.CharField()
    ResourceID = serializers.CharField()
    QualityLevel = serializers.CharField()
   
    DisplayName = serializers.SerializerMethodField('get_displayname')
    LegacyName = serializers.SerializerMethodField('get_legacyname')
    Description = serializers.SerializerMethodField('get_description')
    SharingEnabledDirectories = serializers.SerializerMethodField('get_sharingdirs')
    RDR_Fields = serializers.SerializerMethodField('get_rdr_info')

    @extend_schema_field(OpenApiTypes.STR)
    def get_displayname(self, Endpoint):
        if 'Extension' in Endpoint.AbstractService.EntityJSON.keys():
            if 'go_transfer_xsede_endpoint_displayname' in Endpoint.AbstractService.EntityJSON['Extension'].keys():
                return Endpoint.AbstractService.EntityJSON['Extension']['go_transfer_xsede_endpoint_displayname']
        return ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_legacyname(self, Endpoint):
        if 'Extension' in Endpoint.AbstractService.EntityJSON.keys():
            if 'go_transfer_xsede_endpoint_name' in Endpoint.AbstractService.EntityJSON['Extension'].keys():
                return Endpoint.AbstractService.EntityJSON['Extension']['go_transfer_xsede_endpoint_name']
        return ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, Endpoint):
        if 'Extension' in Endpoint.AbstractService.EntityJSON.keys():
            if 'go_transfer_xsede_endpoint_description' in Endpoint.AbstractService.EntityJSON['Extension'].keys():
                return Endpoint.AbstractService.EntityJSON['Extension']['go_transfer_xsede_endpoint_description']
        return ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_sharingdirs(self, Endpoint):
        if 'Extension' in Endpoint.AbstractService.EntityJSON.keys():
            if 'go_transfer_xsede_share_enabled_directories' in Endpoint.AbstractService.EntityJSON['Extension'].keys():
                return Endpoint.AbstractService.EntityJSON['Extension']['go_transfer_xsede_share_enabled_directories']
        return ''

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_rdr_info(self, Endpoint):
        #rdrinfo = RDRResource.objects.filter(info_resourceid='comet.sdsc.xsede.org').filter(rdr_type='resource')[0]
        #rdrinfo = RDRResource.objects.filter(info_resourceid=Endpoint.ResourceID).filter(rdr_type='resource')[0]
        rdrsearch = RDRResource.objects.filter(info_resourceid=Endpoint.ResourceID).filter(rdr_type='resource')
        if rdrsearch:
            rdrinfo = rdrsearch[0]
        else:
            return ""
        ota = rdrinfo.other_attributes
        organization = ota['organizations'][0]['organization_name']
        org_abbr = ota['organizations'][0]['organization_abbreviation']
        

        return dict([('RDR_DescriptiveName', rdrinfo.resource_descriptive_name), ('RDR_Description', rdrinfo.resource_description), ('RDR_SiteID', rdrinfo.info_siteid), ('Organization_Name', organization), ('Organization_Abbreviation', org_abbr)])

    class Meta:
        model = Endpoint
        fields = ('ResourceID', 'InterfaceName', 'InterfaceVersion', 'URL',
                  'QualityLevel', 'ServingState', 'HealthState', 'ServiceType',
                  'CreationTime', 'ID', 'RDR_Descriptive')
