from django.urls import reverse
from django.utils.encoding import uri_to_iri
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from xcsr_db.models import *
from rest_framework import serializers
from glue2_db.models import AdminDomain

class ComponentSPRequirement_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentSPRequirement
        fields = ('ComponentName', 'SPClass', 'Requirement', 'UpdateTime', 'UpdateUser')
#        fields = ('ComponentName', 'SPClass', 'SPClass_display', 'Requirement', 'Requirement_display', 'UpdateTime', 'UpdateUser')

class SupportContacts_Serializer(serializers.ModelSerializer):
    GlobalID = serializers.SerializerMethodField()
    ShortName = serializers.SerializerMethodField()
    ContactEmail = serializers.SerializerMethodField()
    ContactURL = serializers.SerializerMethodField()
    ContactPhone = serializers.SerializerMethodField()
    DetailURL = serializers.SerializerMethodField()
    @extend_schema_field(OpenApiTypes.STR)
    def get_GlobalID(self,AdminDomain):
        try:
            return AdminDomain.EntityJSON['GlobalID']
        except:
            return None
    @extend_schema_field(OpenApiTypes.STR)
    def get_ShortName(self,AdminDomain):
        try:
            return AdminDomain.EntityJSON['Short Name']
        except:
            return None
    @extend_schema_field(OpenApiTypes.STR)
    def get_ContactEmail(self,AdminDomain):
        try:
            return AdminDomain.EntityJSON['ContactEmail']
        except:
            return None
    @extend_schema_field(OpenApiTypes.STR)
    def get_ContactURL(self,AdminDomain):
        try:
            return AdminDomain.EntityJSON['ContactURL']
        except:
            return None
    @extend_schema_field(OpenApiTypes.STR)
    def get_ContactPhone(self,AdminDomain):
        try:
            return AdminDomain.EntityJSON['ContactPhone']
        except:
            return None
    @extend_schema_field(OpenApiTypes.STR)
    def get_DetailURL(self,AdminDomain):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('supportcontacts-detail', args=[AdminDomain.EntityJSON['GlobalID']])))
        else:
            return ''
    class Meta:
        model = AdminDomain
        fields = ('GlobalID', 'Name', 'Description', 'ShortName', \
                  'ContactEmail', 'ContactURL', 'ContactPhone', \
                  'ID', 'CreationTime', 'DetailURL')
