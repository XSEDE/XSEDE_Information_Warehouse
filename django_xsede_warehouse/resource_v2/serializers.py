from rest_framework import serializers
from resource_v2.models import *
import copy

class Resource_Detail_Serializer(serializers.ModelSerializer):
    # Adds AssociatedResource, Provider fields
    # Adds local field selection
    AssociatedResources = serializers.SerializerMethodField()
    Provider = serializers.SerializerMethodField()
    EntityJSON = serializers.SerializerMethodField()
    def get_AssociatedResources(self, ResourceV2):
        return(self.context.get('associated_resources'))
    def get_Provider(self, ResourceV2):
        try:
            provider = ResourceV2Provider.objects.get(pk=ResourceV2.ProviderID)
            if provider:
                return({'Affiliation': provider.Affiliation, 'LocalID': provider.LocalID, 'Name': provider.Name})
        except ResourceV2Provider.DoesNotExist:
            pass
        return(None)
    def get_EntityJSON(self, ResourceV2):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(ResourceV2.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in ResourceV2.EntityJSON:
                filtered[f] = ResourceV2.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = ResourceV2
        fields = copy.copy([f.name for f in ResourceV2._meta.get_fields(include_parents=False)])
        fields.append('AssociatedResources')
        fields.append('Provider')

class Resource_Search_Serializer(serializers.ModelSerializer):
    # Adds Provider field
    # Adds local field selection
    Provider = serializers.SerializerMethodField()
    EntityJSON = serializers.SerializerMethodField()
    def get_Provider(self, ResourceV2):
        try:
            provider = ResourceV2Provider.objects.get(pk=ResourceV2.ProviderID)
            if provider:
                return({'Affiliation': provider.Affiliation, 'LocalID': provider.LocalID, 'Name': provider.Name})
        except ResourceV2Provider.DoesNotExist:
            pass
        return(None)
    def get_EntityJSON(self, ResourceV2):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(ResourceV2.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in ResourceV2.EntityJSON:
                filtered[f] = ResourceV2.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = ResourceV2
        fields = copy.copy([f.name for f in ResourceV2._meta.get_fields(include_parents=False)])
        fields.append('Provider')

class Resource_Event_Serializer(serializers.ModelSerializer):
    # Adds local field selection
    EntityJSON = serializers.SerializerMethodField()
    def get_EntityJSON(self, ResourceV2):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(ResourceV2.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in ResourceV2.EntityJSON:
                filtered[f] = ResourceV2.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = ResourceV2
        fields = ('__all__')

class Resource_Types_Serializer(serializers.Serializer):
    Type = serializers.CharField()
    count = serializers.IntegerField()
    class Meta:
        fields = ('__all__')

class ResourceProvider_Search_Serializer(serializers.ModelSerializer):
    # Adds local field selection
    EntityJSON = serializers.SerializerMethodField()
    def get_EntityJSON(self, ResourceV2):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(ResourceV2.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in ResourceV2.EntityJSON:
                filtered[f] = ResourceV2.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = ResourceV2Provider
        fields = ('__all__')
