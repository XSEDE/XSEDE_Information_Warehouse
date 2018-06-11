from projectresources.models import *
from rest_framework import serializers

class ProjectResource_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectResource
        fields = ('project_number','ResourceID')
