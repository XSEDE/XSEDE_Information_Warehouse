from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rdr_db.models import *
from rdr_db.serializers import *
import pdb

# Create your views here.
class RDRResource_List(APIView):
    '''
        All RDR resources
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        if 'resourceid' in self.kwargs:
            objects = RDRResource.objects.filter(info_resourceid__exact=self.kwargs['resourceid'])
        elif 'siteid' in self.kwargs:
            objects = RDRResource.objects.filter(info_siteid__exact=self.kwargs['siteid'])
        elif 'rdrtype' in self.kwargs:
            objects = RDRResource.objects.filter(rdr_type__exact=self.kwargs['rdrtype'])
        else:
            objects = RDRResource.objects.all()
        try:
            sort_by = request.GET.get('sort')
            objects_sorted = objects.order_by(sort_by)
        except:
            objects_sorted = objects

        returnformat = request.query_params.get('format', 'json')
        if returnformat != 'html':
            serializer = RDRResource_Serializer(objects_sorted, many=True)
            return Response(serializer.data)
        else:
            serializer = RDRResource_Serializer_Plus(objects_sorted, context={'request': request}, many=True)
            return render(request, 'rdr_db/list.html', {'resource_list': serializer.data})

class RDRResource_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
#    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        pdb.set_trace()
        if 'id' in self.kwargs:
            try:
                object = RDRResource.objects.get(pk=self.kwargs['id'])
            except RDRResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RDRResource_Serializer_Plus(object)
        returnformat = request.query_params.get('format', 'json')
        if returnformat != 'html':
            return Response(serializer.data)
        else:
            return render(request, 'rdr_db/detail.html', {'resource_list': [serializer.data]})

class RDRResource_XUP_List(APIView):
    '''
        All RDR resources for the XUP
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request, format=None):
        objects = RDRResource.objects.all()
        serializer = RDRResource_Serializer(objects, many=True)
        return Response(serializer.data)

class RDRResource_XUP_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
#       pdb.set_trace()
        if 'id' in self.kwargs:
            try:
                object = RDRResource.objects.get(pk=self.kwargs['id'])
            except RDRResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = RDRResource_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = RDRResource.objects.filter(info_resourceid__exact=self.kwargs['resourceid'])
            serializer = RDRResource_Serializer(objects, many=True)
        return Response(serializer.data)


