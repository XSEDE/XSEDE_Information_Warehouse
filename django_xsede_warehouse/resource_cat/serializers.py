from rest_framework import serializers
from resource_cat.models import *
import copy

class Resource_Detail_Serializer(serializers.ModelSerializer):
    # Adds AssociatedResource, Provider fields
    # Adds local field selection
    AssociatedResources = serializers.SerializerMethodField()
    Provider = serializers.SerializerMethodField()
    EntityJSON = serializers.SerializerMethodField()
    def get_AssociatedResources(self, Resource):
        return(self.context.get('associated_resources'))
    def get_Provider(self, Resource):
        try:
            provider = ResourceProvider.objects.get(pk=Resource.ProviderID)
            if provider:
                return({'Affiliation': provider.Affiliation, 'LocalID': provider.LocalID, 'Name': provider.Name})
        except ResourceProvider.DoesNotExist:
            pass
        return(None)
    def get_EntityJSON(self, Resource):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(Resource.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in Resource.EntityJSON:
                filtered[f] = Resource.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = Resource
        fields = copy.copy([f.name for f in Resource._meta.get_fields(include_parents=False)])
        fields.append('AssociatedResources')
        fields.append('Provider')

class Resource_Search_Serializer(serializers.ModelSerializer):
    # Adds Provider field
    # Adds local field selection
    Provider = serializers.SerializerMethodField()
    EntityJSON = serializers.SerializerMethodField()
    def get_Provider(self, Resource):
        try:
            provider = ResourceProvider.objects.get(pk=Resource.ProviderID)
            if provider:
                return({'Affiliation': provider.Affiliation, 'LocalID': provider.LocalID, 'Name': provider.Name})
        except ResourceProvider.DoesNotExist:
            pass
        return(None)
    def get_EntityJSON(self, Resource):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(Resource.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in Resource.EntityJSON:
                filtered[f] = Resource.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = Resource
        fields = copy.copy([f.name for f in Resource._meta.get_fields(include_parents=False)])
        fields.append('Provider')

class Resource_Event_Serializer(serializers.ModelSerializer):
    # Adds local field selection
    EntityJSON = serializers.SerializerMethodField()
    def get_EntityJSON(self, Resource):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(Resource.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in Resource.EntityJSON:
                filtered[f] = Resource.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = Resource
        fields = ('__all__')

class Resource_Types_Serializer(serializers.Serializer):
    Type = serializers.CharField()
    count = serializers.IntegerField()
    class Meta:
        fields = ('__all__')

class ResourceProvider_Search_Serializer(serializers.ModelSerializer):
    # Adds local field selection
    EntityJSON = serializers.SerializerMethodField()
    def get_EntityJSON(self, Resource):
        want_fields = self.context.get('fields')
        if len(want_fields) == 0 or '__local__' in want_fields:
            return(Resource.EntityJSON)
        filtered = {}
        for f in want_fields.union(['id']):     # Add 'id'
            if f in Resource.EntityJSON:
                filtered[f] = Resource.EntityJSON.get(f)
        return(filtered)
    class Meta:
        model = ResourceProvider
        fields = ('__all__')
