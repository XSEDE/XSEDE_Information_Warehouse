from django.urls import reverse
from django.utils.encoding import uri_to_iri
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import *
import copy

class Catalog_List_Serializer(serializers.ModelSerializer):
    DetailURL = serializers.SerializerMethodField()
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_DetailURL(self, ResourceV3Catalog):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('catalog-detail', args=[ResourceV3Catalog.ID])))
        else:
            return ''

    class Meta:
        model = ResourceV3Catalog
        fields = copy.copy([f.name for f in ResourceV3Catalog._meta.get_fields(include_parents=False)])
        fields.append('DetailURL')

class Catalog_Detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceV3Catalog
        fields = ('__all__')

class Local_List_Serializer(serializers.ModelSerializer):
    DetailURL = serializers.SerializerMethodField()
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_DetailURL(self, ResourceV3Local):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('local-detail-globalid', args=[ResourceV3Local.ID])))
        else:
            return ''

    class Meta:
        model = ResourceV3Local
        fields = copy.copy([f.name for f in ResourceV3Local._meta.get_fields(include_parents=False)])
        fields.append('DetailURL')

class Local_Detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceV3Local
        fields = ('__all__')

#
# UNCONVERTED
#

class Resource_Detail_Serializer(serializers.ModelSerializer):
    # Adds Relations
    # Adds local raw EntityJSON
    Relations = serializers.SerializerMethodField()
    DetailURL = serializers.SerializerMethodField()
    EntityJSON = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_Relations(self, ResourceV3):
        relations = []
        http_request = self.context.get('request')
        try:
            relateditems = ResourceV3Relation.objects.filter(FirstResourceID=ResourceV3.ID)
            for ri in relateditems:
                related = {'RelationType': ri.RelationType, 'ID': ri.SecondResourceID}
                provider = ResourceV3Index.Lookup_Relation(ri.SecondResourceID)
                if provider and provider.get('Name'):
                    related['Name'] = provider.get('Name')
                if provider and provider.get('ResourceGroup'):
                    related['ResourceGroup'] = provider.get('ResourceGroup')
                if provider and provider.get('ProviderID'):
                    rp = ResourceV3Index.Lookup_Relation(provider.get('ProviderID'))
                    if rp and rp.get('Name'):
                        related['Provider'] = rp.get('Name')
                if http_request:
                    related['DetailURL'] = http_request.build_absolute_uri(uri_to_iri(reverse('resource-detail', args=[ri.SecondResourceID])))
                relations.append(related)
        except ResourceV3Relation.DoesNotExist:
            pass
# Excluding Inverse Relations for now, consider adding including as InverseRelations in the future
#        try:
#            related = ResourceV3Relation.objects.filter(SecondResourceID=ResourceV3.ID)
#            for ri in related:
#                relations.append({"Type": ri.RelationType, "From.ID": ri.FirstResourceID})
#        except ResourceV3Relation.DoesNotExist:
#            pass
        return(relations)

    @extend_schema_field(OpenApiTypes.STR)
    def get_DetailURL(self, ResourceV3):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('resource-detail', args=[ResourceV3.ID])))
        else:
            return ''

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_EntityJSON(self, ResourceV3):
        try:
            local = ResourceV3Local.objects.get(pk=ResourceV3.ID)
            return(local.EntityJSON)
        except ResourceV3Local.DoesNotExist:
            pass
        return(none)

    class Meta:
        model = ResourceV3
        fields = copy.copy([f.name for f in ResourceV3._meta.get_fields(include_parents=False)])
        fields.append('Relations')
        fields.append('DetailURL')
        fields.append('EntityJSON')

class Resource_Search_Serializer(serializers.ModelSerializer):
    # Adds Provider field
    # Adds local field selection
    Provider = serializers.SerializerMethodField()
    DetailURL = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_Provider(self, ResourceV3):
#        try:
#            provider = ResourceV3Provider.objects.get(pk=ResourceV3.ProviderID)
#            if provider:
#                return({'Affiliation': provider.Affiliation, 'LocalID': provider.LocalID, 'Name': provider.Name})
#        except ResourceV3Provider.DoesNotExist:
#            pass
        return(None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_DetailURL(self, ResourceV3):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('resource-detail', args=[ResourceV3.ID])))
        else:
            return ''

    class Meta:
        model = ResourceV3
        fields = copy.copy([f.name for f in ResourceV3._meta.get_fields(include_parents=False)])
        fields.append('Provider')
        fields.append('DetailURL')

class Resource_ESearch_Serializer(serializers.ModelSerializer):
#    score = serializers.SerializerMethodField()
#    def get_score(self, ResourceV3):
#        return(ResourceV3.meta.score)
    class Meta:
        model = ResourceV3Index
        fields = ('__all__')
#        fields = copy.copy([f.name for f in ResourceV3Index._meta.get_fields(include_parents=False)])
#        fields.append('score')

class Resource_Event_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceV3
        fields = ('__all__')

class Resource_Types_Serializer(serializers.Serializer):
    ResourceGroup = serializers.CharField()
    Type = serializers.CharField()
    count = serializers.IntegerField()

    class Meta:
        fields = ('__all__')
