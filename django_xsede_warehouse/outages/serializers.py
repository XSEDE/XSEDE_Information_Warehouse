from outages.models import *
from rest_framework import serializers

class Outages_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Outages
        fields = ('__all__')
