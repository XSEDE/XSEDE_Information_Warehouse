from rdr_db.models import *
from rest_framework import serializers
from django.utils.encoding import uri_to_iri
from django.urls import reverse, get_script_prefix
import copy

class RDRResource_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RDRResource
        fields = ('__all__')

class RDRResource_Serializer_Plus(serializers.ModelSerializer):
    DetailURL = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z')
    
    def get_DetailURL(self, RDRResource):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('rdr-detail', args=[RDRResource.rdr_resource_id])))
        else:
            return ''
    
    class Meta:
        model = RDRResource
        fields = copy.copy([f.name for f in RDRResource._meta.get_fields(include_parents=False)])
        fields.append('DetailURL')

class RDR_CSA_Serializer(serializers.ModelSerializer):
    csa_feature_user_description = serializers.SerializerMethodField()
    csa_email = serializers.SerializerMethodField()
    gateway_recommended_use = serializers.SerializerMethodField()
    gateway_support_attributes = serializers.SerializerMethodField()
    
    def get_csa_feature_user_description(self, RDRResource):
        return RDRResource.other_attributes['community_software_area_feature_user_description']
    def get_csa_email(self, RDRResource):
        return RDRResource.other_attributes['community_software_area_email']
    def get_gateway_recommended_use(self, RDRResource):
        return RDRResource.other_attributes['gateway_recommended_use']
    def get_gateway_support_attributes(self, RDRResource):
        try:
            return ', '.join(RDRResource.other_attributes['gateway_support']['gateway_support_attributes'])
        except:
            return None
    
    class Meta:
        model = RDRResource
        fields = ['info_resourceid', 'resource_descriptive_name', 'resource_description', 'gateway_recommended_use', 'gateway_support_attributes',
            'csa_feature_user_description', 'csa_email' ]
