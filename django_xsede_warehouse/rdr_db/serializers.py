from rdr_db.models import *
from rest_framework import serializers
import pdb

class RDRResource_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RDRResource
        fields = ('__all__')

class RDRResource_Serializer_Plus(serializers.ModelSerializer):
    Active = serializers.SerializerMethodField()
    
    def get_Active(self, RDRResource):
        return RDRResource.Active
    
    class Meta:
        model = RDRResource
        fields = RDRResource._meta.get_all_field_names().append('Active')
