from django.db.models import Q
from django.core.serializers import serialize
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import uri_to_iri

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rdr_db.models import RDRResource
from rdr_db.filters import *
from glue2_db.models import ApplicationHandle
from xdcdb.models import *
from xdcdb.serializers import *
from rdr_db.serializers import *
from warehouse_views.serializers import Generic_Resource_Serializer, Software_Full_Serializer
import pdb

# Create your views here.
class Resource_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        returnformat = request.query_params.get('format', None)
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='ALL', result='RESOURCEID')
        objects = RDRResource.objects.filter(rdr_type='resource').order_by('info_resourceid')
        for o in objects:
            o.Active = o.info_resourceid in active_resourceids
        if returnformat == 'json':
            serializer = RDRResource_Serializer_Plus(objects, many=True)
            return Response(serializer.data)
        else:
            c = Context({'resource_list': objects})
            return render(request, 'warehouse_resources.html', c)

class Resource_List_Active(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        returnformat = request.query_params.get('format', None)
        objects = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='SUB', result='OBJECTS').order_by('info_resourceid')
        for o in objects:
            o.Active = True
        if returnformat == 'json':
            serializer = RDRResource_Serializer_Plus(objects, many=True)
            return Response(serializer.data)
        else:
            c = Context({'resource_list': objects})
            return render(request, 'warehouse_resources.html', c)

class Resource_List_XDCDB_Active(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        returnformat = request.query_params.get('format', None)
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='ALL', result='RESOURCEID')
        objects = TGResource.objects.filter(ResourceID__in=active_resourceids).order_by('ResourceID')
        if returnformat == 'json':
            serializer = XcdbResource_Serializer(objects, many=True)
            return Response(serializer.data)
        else:
            c = Context({'xdcdb_list': objects})
            return render(request, 'xdcdb_resources.html', c)

class Resource_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
#    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
#        pdb.set_trace()
        returnformat = request.query_params.get('format', None)
        if 'resourceid' in self.kwargs:
            try:
                objects = RDRResource.objects.filter(info_resourceid__exact=uri_to_iri(self.kwargs['resourceid']),rdr_type__exact='resource')
            except RDRResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if returnformat == 'json':
            serializer = Generic_Resource_Serializer(objects[0])
            return Response(serializer.data)
        else:
            serializer = Generic_Resource_Serializer(objects[0])
            c = Context({'resource_details': serializer.data})
            return render(request, 'resource_details.html', c)

class Software_Full(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = ApplicationHandle.objects.get(pk=uri_to_iri(self.kwargs['id'])) # uri_to_iri translates %xx
            except ApplicationHandle.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = Software_Full_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            serializer = Software_Full_Serializer(objects, many=True)
#        elif 'siteid' in self.kwargs:
#            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['siteid'])
#            serializer = Software_Full_Serializer(objects, many=True)
        elif 'appname' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ApplicationEnvironment__AppName__exact=uri_to_iri(self.kwargs['appname']))
            serializer = Software_Full_Serializer(objects, many=True)
        else:
            objects = ApplicationHandle.objects.all()
            serializer = Software_Full_Serializer(objects, many=True)
        return Response(serializer.data)

class Software_XUP_v1_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
#        active_resourceids = Active_ResourceIDs()
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='SUB', result='RESOURCEID')
        objects = ApplicationHandle.objects.filter(ResourceID__in=active_resourceids)
        serializer = Software_Full_Serializer(objects, many=True)
        return Response(serializer.data)
