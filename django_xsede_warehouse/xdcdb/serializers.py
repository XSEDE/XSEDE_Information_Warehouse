from rest_framework import serializers
from xdcdb.models import *
from glue2_db.models import *
from glue2_db.serializers import *
from django.utils.encoding import uri_to_iri
from django.urls import reverse, get_script_prefix
import copy

class XSEDEResource_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TGResource
        fields = ('__all__')

class XSEDEResource_DetailURL_Serializer(serializers.ModelSerializer):
    Timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z')
    DetailURL = serializers.SerializerMethodField()
    
    def get_DetailURL(self, TGResource):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('xdcdb-resource-detail', args=[TGResource.ResourceID])))
        else:
            return ''
    class Meta:
        model = TGResource
        fields = copy.copy([f.name for f in TGResource._meta.get_fields(include_parents=False)])
        fields.append('DetailURL')


class XSEDEResourcePublished_Serializer(serializers.Serializer):
    ResourceID = serializers.CharField()
    ResourceName = serializers.SerializerMethodField('get_resourcename')
    SiteID = serializers.CharField()
    ResourceKits = serializers.SerializerMethodField('get_resourcekits')
    OrganizationAbbrev = serializers.CharField()
    OrganizationName = serializers.CharField()
    AmieName = serializers.CharField()
    PopsName = serializers.CharField()
    TgcdbResourceName = serializers.CharField()
    ResourceCode = serializers.CharField()
    ResourceDescription = serializers.CharField()
    Timestamp = serializers.DateTimeField()
    
    def get_resourcename(self, TGResource):
        glue2search = ApplicationEnvironment.objects.filter(ResourceID=TGResource.ResourceID)
        if glue2search:
            glue2info = glue2search[0]
        else:
            return ""
        return glue2info.Name 
    def get_resourcekits(self, TGResource):
        glue2search = ApplicationEnvironment.objects.filter(ResourceID=TGResource.ResourceID)
        if glue2search:
            return "true"
        else:
            return "false"
    class Meta:
        model = TGResource
        fields = ('ResourceID', 'SiteID', 'OrganizationAbbrev', 
                  'OrganizationName', 'AmieName', 'PopsName',
                  'TgcdbResourceName', 'ResourceCode', 
                  'ResourceDescription', 'Timestamp')

class XSEDEPerson_Serializer(serializers.Serializer):
    person_id = serializers.IntegerField()
    portal_login = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    is_suspended = serializers.BooleanField()
    organization = serializers.CharField()
    citizenships = serializers.CharField()
    emails = serializers.CharField()
    addressesJSON = serializers.JSONField()
    DetailURL = serializers.SerializerMethodField()
    
    def get_DetailURL(self, XSEDEPerson):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('xsede-person-detail', args=[XSEDEPerson.person_id])))
        else:
            return ''

    class Meta:
        model = XSEDEPerson
        fields = ('person_id', 'portal_login', 'last_name', 'first_name', 'middle_name',
            'is_suspended', 'organization', 'citizenships', 'emails', 'addressesJSON', 'DetailURL')
