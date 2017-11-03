from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from glue2_db.models import ApplicationEnvironment, AbstractService, ComputingQueue, Endpoint
from glue2_views_api.serializers import *
from xsede_warehouse.responses import MyAPIResponse

# Create your views here.
class ApplicationEnvironment_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ApplicationEnvironment.objects.all()
        serializer = ApplicationEnvironment_Serializer(objects, many=True)
        return Response(serializer.data)

# Software information comes from ApplicationHandle and the related ApplicationEnvironment
class Software_List(APIView):
    '''
        GLUE2 software combining ApplicationEnvironment and AppliactionHandle
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ApplicationHandle.objects.all()
        serializer = ApplicationHandle_Serializer(objects, many=True)
        return Response(serializer.data)

class Software_Detail(APIView):
    '''
        GLUE2 software combining ApplicationEnvironment and AppliactionHandle
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = ApplicationHandle.objects.get(pk=uri_to_iri(self.kwargs['id'])) # uri_to_iri translates %xx
            except ApplicationHandle.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ApplicationHandle_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            serializer = ApplicationHandle_Serializer(objects, many=True)
        elif 'appname' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ApplicationEnvironment__AppName__exact=uri_to_iri(self.kwargs['appname']))
            serializer = ApplicationHandle_Serializer(objects, many=True)
        return Response(serializer.data)

# Service information comes from Endpoint and the parent AbstractService
class Services_List(APIView):
    '''
        GLUE2 services combining AbstractService and Endpoint
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = Endpoint.objects.all()
        serializer = EndpointServices_Serializer(objects, many=True)
        return Response(serializer.data)

class Services_Detail(APIView):
    '''
        GLUE2 services combining AbstractService and Endpoint
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = Endpoint.objects.get(pk=self.kwargs['id'])
            except Endpoint.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = EndpointServices_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = Endpoint.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            serializer = EndpointServices_Serializer(objects, many=True)
        elif 'interfacename' in self.kwargs:
            objects = Endpoint.objects.filter(InterfaceName__exact=self.kwargs['interfacename'])
            serializer = EndpointServices_Serializer(objects, many=True)
        elif 'servicetype' in self.kwargs:
            objects = Endpoint.objects.filter(AbstractService__ServiceType__exact=self.kwargs['servicetype'])
            serializer = EndpointServices_Serializer(objects, many=True)
        return Response(serializer.data)

class Jobs_List(APIView):
    '''
        GLUE2 Jobs from ComputingQueue
    '''
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'resourceid' in self.kwargs:
            try:
                objects = ComputingQueue.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            except ComputingQueue.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            objects = ComputingQueue.objects.all()
        try:
            sort_by = request.GET.get('sort')
        except:
            sort_by = None
        serializer = ComputingQueue_Expand_Serializer(objects, many=True, context={'sort_by': sort_by})
        return MyAPIResponse({'result_set': serializer.data}, template_name='glue2_views_api/jobs.html')
