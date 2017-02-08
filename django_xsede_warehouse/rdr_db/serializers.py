from rdr_db.models import *
from rest_framework import serializers
import copy
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
        fields = copy.copy([f.name for f in RDRResource._meta.get_fields(include_parents=False)])
        fields.append('Active')
