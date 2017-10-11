from rdr_db.models import *
from rest_framework import serializers
from django.utils.encoding import uri_to_iri
from django.core.urlresolvers import reverse, get_script_prefix
import copy
import pdb

class RDRResource_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RDRResource
        fields = ('__all__')

class RDRResource_Serializer_Plus(serializers.ModelSerializer):
    DetailURL = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S %Z')
    
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
