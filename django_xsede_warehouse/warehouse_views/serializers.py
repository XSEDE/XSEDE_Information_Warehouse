from rest_framework import serializers
#from drf_toolbox import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rdr_db.models import RDRResource
from xdcdb.models import TGResource
from glue2_db.models import ApplicationEnvironment, ApplicationHandle
from glue2_db.serializers import ApplicationHandle_DbSerializer
import pdb

#class JSONSerializerField(serializers.Field):
#    """ Serializer for JSONField -- required to make field writable"""
#    def to_internal_value(self, data):
#        return data
#    def to_representation(self, value):
#        return value


class Generic_Resource_Serializer(serializers.ModelSerializer):
    # Note: recommended_use and access_description come from compute sub-resources
    ResourceID = serializers.CharField(source='info_resourceid')
    SiteID = serializers.CharField(source='info_siteid')
    OrganizationAbbrev = serializers.SerializerMethodField()
    OrganizationName = serializers.SerializerMethodField()
    AmieName = serializers.SerializerMethodField()
    PopsName = serializers.SerializerMethodField()
    XcdbName = serializers.SerializerMethodField()
    class Meta:
        model = RDRResource
        fields = ('ResourceID', 'SiteID',
                  'rdr_resource_id', 'rdr_type', 'parent_resource',
                  'resource_descriptive_name', 'resource_description',
                  'current_statuses', 'latest_status', 'latest_status_begin', 'latest_status_end',
                  'recommended_use', 'access_description',
                  'project_affiliation', 'provider_level', 'updated_at',
                  'OrganizationAbbrev', 'OrganizationName',
                  'AmieName','PopsName', 'XcdbName')

    def get_OrganizationAbbrev(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.OrganizationAbbrev
        except TGResource.DoesNotExist:
            pass
        return None
    def get_OrganizationName(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.OrganizationName
        except TGResource.DoesNotExist:
            pass
        return None
    def get_AmieName(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.AmieName
        except TGResource.DoesNotExist:
            pass
        return None
    def get_PopsName(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.PopsName
        except TGResource.DoesNotExist:
            pass
        return None
    def get_XcdbName(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.TgcdbResourceName
        except TGResource.DoesNotExist:
            pass
        return None

class Software_Full_Serializer(serializers.ModelSerializer):
#    pdb.set_trace()
    SiteID = serializers.SerializerMethodField('get_siteid')
    AppName = serializers.CharField(source='ApplicationEnvironment.AppName')
    AppVersion = serializers.CharField(source='ApplicationEnvironment.AppVersion')
    Description = serializers.CharField(source='ApplicationEnvironment.Description')
    Handle = serializers.SerializerMethodField('get_handle')
    Domain = serializers.SerializerMethodField('get_category')
    Keywords = serializers.SerializerMethodField('get_keywords')
    class Meta:
        model = ApplicationHandle
        fields = ('ResourceID', 'SiteID', 'AppName', 'AppVersion', 'Description', 'Handle',
                  'Domain', 'Keywords', 'CreationTime','ID')

    def get_siteid(self, ApplicationHandle):
        try:
            RDR_object = RDRResource.objects.filter(rdr_type='resource').filter(info_resourceid=ApplicationHandle.ResourceID)
            if RDR_object and RDR_object[0] and RDR_object[0].info_siteid:
                return RDR_object[0].info_siteid
        except RDRResource.DoesNotExist:
            pass
        return None

    def get_handle(self, ApplicationHandle):
        return({'HandleType': ApplicationHandle.Type,
                'HandleKey': ApplicationHandle.Value
               })
    
    def get_category(self, ApplicationHandle):
        if 'Extension' in ApplicationHandle.ApplicationEnvironment.EntityJSON.keys() and 'Category' in ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension'].keys():
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension']['Category']
        else:
            return []

    def get_keywords(self, ApplicationHandle):
#        if 'Extension' in ApplicationHandle.ApplicationEnvironment.EntityJSON.keys()
#           and 'Keywords' in ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension'].keys():
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension']['Keywords']
        except:
            return []
