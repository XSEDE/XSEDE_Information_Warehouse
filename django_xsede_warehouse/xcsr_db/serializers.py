from xcsr_db.models import *
from rest_framework import serializers

class ComponentSPRequirement_Serializer(serializers.ModelSerializer):
#    SPClass = serializers.ChoiceField(choices=ComponentSPRequirement.SPClass_CHOICES, default='xfl3')
#    SPClass_display = serializers.CharField(source='get_SPClass_display', read_only=True)
#    Requirement = serializers.ChoiceField(choices=ComponentSPRequirement.Requirement_CHOICES, default='R')
#    Requirement_display = serializers.CharField(source='get_Requirement_display', read_only=True)

    class Meta:
        model = ComponentSPRequirement
        fields = ('ComponentName', 'SPClass', 'Requirement', 'UpdateTime', 'UpdateUser')
#        fields = ('ComponentName', 'SPClass', 'SPClass_display', 'Requirement', 'Requirement_display', 'UpdateTime', 'UpdateUser')