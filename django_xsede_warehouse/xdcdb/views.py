from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from xdcdb.models import *
from xdcdb.serializers import *

# Create your views here.
class TGResource_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = TGResource.objects.all()
        serializer = TGResource_Serializer(objects, many=True)
        return Response(serializer.data)

class TGResource_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = TGResource.objects.get(pk=self.kwargs['id'])
            except Endpoint.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = TGResource_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = TGResource.objects.filter(info_resourceid__exact=self.kwargs['resourceid'])
            serializer = TGResource_Serializer(objects, many=True)
        return Response(serializer.data)

class TGResourcePublished_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get (self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object=TGResource.objects.get(pk=self.kwargs['id'])
            except TGResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = TGResourcePublished_Serializer(object)
        return Response(serializer.data)
