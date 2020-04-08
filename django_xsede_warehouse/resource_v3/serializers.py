from django.urls import reverse
from django.utils.encoding import uri_to_iri
from rest_framework import serializers
from .models import *
import copy

class Catalog_List_Serializer(serializers.ModelSerializer):
    DetailURL = serializers.SerializerMethodField()
    
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
    # Adds AssociatedResource
    # Adds local raw EntityJSON
    RelatedResources = serializers.SerializerMethodField()
    EntityJSON = serializers.SerializerMethodField()
    def get_RelatedResources(self, ResourceV3):
        relations = []
        try:
            related = ResourceV3Relation.objects.filter(FirstResourceID=ResourceV3.ID)
            for ri in related:
                relations.append({"Type": ri.RelationType, "To.ID": ri.SecondResourceID})
        except ResourceV3Relation.DoesNotExist:
            pass
        try:
            related = ResourceV3Relation.objects.filter(SecondResourceID=ResourceV3.ID)
            for ri in related:
                relations.append({"Type": ri.RelationType, "From.ID": ri.SecondResourceID})
        except ResourceV3Relation.DoesNotExist:
            pass
        return(relations)
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
        fields.append('RelatedResources')
        fields.append('EntityJSON')

class Resource_Search_Serializer(serializers.ModelSerializer):
    # Adds Provider field
    # Adds local field selection
    Provider = serializers.SerializerMethodField()
    def get_Provider(self, ResourceV3):
#        try:
#            provider = ResourceV3Provider.objects.get(pk=ResourceV3.ProviderID)
#            if provider:
#                return({'Affiliation': provider.Affiliation, 'LocalID': provider.LocalID, 'Name': provider.Name})
#        except ResourceV3Provider.DoesNotExist:
#            pass
        return(None)
    class Meta:
        model = ResourceV3
        fields = copy.copy([f.name for f in ResourceV3._meta.get_fields(include_parents=False)])
        fields.append('Provider')

class Resource_ESearch_Serializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    def get_score(self, ResourceV3):
        return(ResourceV3.meta.score)
    class Meta:
        model = ResourceV3
        fields = copy.copy([f.name for f in ResourceV3._meta.get_fields(include_parents=False)])
        fields.append('score')

class Resource_Event_Serializer(serializers.ModelSerializer):
    # Adds local field selection
    EntityJSON = serializers.SerializerMethodField()
    def get_EntityJSON(self, ResourceV3):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(ResourceV3.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in ResourceV3.EntityJSON:
                filtered[f] = ResourceV3.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = ResourceV3
        fields = ('__all__')

class Resource_Types_Serializer(serializers.Serializer):
    ResourceGroup = serializers.CharField()
    Type = serializers.CharField()
    count = serializers.IntegerField()
    class Meta:
        fields = ('__all__')

class Provider_Detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceV3
        fields = copy.copy([f.name for f in ResourceV3._meta.get_fields(include_parents=False)])

class Provider_List_Serializer(serializers.ModelSerializer):
#    # Adds local field selection
#    EntityJSON = serializers.SerializerMethodField()
#    def get_EntityJSON(self, ResourceV3):
#        want_fields = self.context.get('fields')
#        if len(want_fields) == 0 or '__local__' in want_fields:
#            return(ResourceV3.EntityJSON)
#        filtered = {}
#        for f in want_fields.union(['id']):     # Add 'id'
#            if f in ResourceV3.EntityJSON:
#                filtered[f] = ResourceV3.EntityJSON.get(f)
#        return(filtered)
    class Meta:
        model = ResourceV3
        fields = ('__all__')

class Guide_Detail_Serializer(serializers.ModelSerializer):
    # Adds local field selection
    EntityJSON = serializers.SerializerMethodField()
    def get_EntityJSON(self, ResourceV3):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(ResourceV3.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in ResourceV3.EntityJSON:
                filtered[f] = ResourceV3.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = ResourceV3
        fields = copy.copy([f.name for f in ResourceV3._meta.get_fields(include_parents=False)])

class Guide_Search_Serializer(serializers.ModelSerializer):
    # Adds local field selection
    EntityJSON = serializers.SerializerMethodField()
    def get_EntityJSON(self, ResourceV3):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(ResourceV3.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in ResourceV3.EntityJSON:
                filtered[f] = ResourceV3.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = ResourceV3
        fields = copy.copy([f.name for f in ResourceV3._meta.get_fields(include_parents=False)])
