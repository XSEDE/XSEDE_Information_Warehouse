from rdr_db.models import *
from rest_framework import serializers

class RDRResource_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RDRResource
        fields = ('__all__')