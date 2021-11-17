from django.http import *
from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from drf_spectacular.utils import extend_schema

# Create your views here.
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from goendpoint_api.serializers import *
from glue2_db.models import *
from glue2_db.serializers import *
from rdr_db.models import *
from rdr_db.serializers import *
#from goendpoint_api.models import *

#from django.core.urlresolvers import resolve
import logging
logg2 = logging.getLogger('xsede.logger')

#Service information comes from Endpoint and the parent AbstractService
class goServices_List(APIView):
    '''
        Globus Online endpoints derived from GLUE2 Endpoint
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=goEndpointServices_Serializer)
    def get(self, request, format=None):
        endpoints = Endpoint.objects.filter(Name__exact='org.globus.gridftp')
        serializer = goEndpointServices_Serializer(endpoints,many=True)
        return Response(serializer.data)

class goServices_Detail(APIView):
    '''
        Globus Online endpoints derived from GLUE2 Endpoint
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=goEndpointServices_Serializer)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = Endpoint.objects.get(pk=self.kwargs['id'])
            except Endpoint.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = goEndpointServices_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = Endpoint.objects.filter(ResourceID__exact=self.kwargs['resourceid']).filter(Name__exact='org.globus.gridftp')
            serializer = goEndpointServices_Serializer(objects, many=True)
        elif 'interfacename' in self.kwargs:
            objects = Endpoint.objects.filter(InterfaceName__exact=self.kwargs['interfacename']).filter(Name__exact='org.globus.gridftp')
            serializer = goEndpointServices_Serializer(objects, many=True)
        elif 'servicetype' in self.kwargs:
            objects = Endpoint.objects.filter(AbstractService__ServiceType__exact=self.kwargs['servicetype']).filter(Name__exact='org.globus.gridftp')
            serializer = goEndpointServices_Serializer(objects, many=True)
        return Response(serializer.data)

