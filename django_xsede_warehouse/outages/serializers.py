from rest_framework import serializers
from outages.models import *
from django.utils.encoding import uri_to_iri
from django.core.urlresolvers import reverse, get_script_prefix
import copy

class Outages_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Outages
        fields = ('__all__')

class Outages_DetailURL_Serializer(serializers.ModelSerializer):
    OutageStart = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S %Z')
    OutageEnd = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S %Z')
    DetailURL = serializers.SerializerMethodField()
    
    def get_DetailURL(self, Outages):
        http_request = self.context.get('request')
        if http_request:
            return http_request.build_absolute_uri(uri_to_iri(reverse('outages-detail', args=[Outages.ID])))
        else:
            return ''
    class Meta:
        model = Outages
        fields = copy.copy([f.name for f in Outages._meta.get_fields(include_parents=False)])
        fields.append('DetailURL')
