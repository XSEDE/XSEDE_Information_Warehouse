from rest_framework import serializers
from xdcdb.models import *
from glue2_db.models import *
from glue2_db.serializers import *
from django.utils.encoding import uri_to_iri
from django.core.urlresolvers import reverse, get_script_prefix
import copy

class XcdbResource_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TGResource
        fields = ('__all__')

class XcdbResource_DetailURL_Serializer(serializers.ModelSerializer):
    Timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z')
    DetailURL = serializers.SerializerMethodField()
    
    def get_DetailURL(self, TGResource):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('xdcdb-detail', args=[TGResource.ResourceID])))
        else:
            return ''
    class Meta:
        model = TGResource
#        fields = ('__all__', 'DetailURL')
        fields = copy.copy([f.name for f in TGResource._meta.get_fields(include_parents=False)])
        fields.append('DetailURL')


class XcdbResourcePublished_Serializer(serializers.Serializer):
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
