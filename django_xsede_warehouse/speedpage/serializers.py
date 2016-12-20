from speedpage.models import *
from rest_framework import serializers

class speedpage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = speedpage
        fields = ('__all__')
