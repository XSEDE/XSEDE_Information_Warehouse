from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rdr_db.models import *
from rdr_db.serializers import *

# Create your views here.
class RDRResource_XUP_List(APIView):
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