from xdcdb.models import *
from glue2_db.models import *
from glue2_db.serializers import *
from rest_framework import serializers

class TGResource_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TGResource
        fields = ('__all__')

class TGResourcePublished_Serializer(serializers.Serializer):
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
