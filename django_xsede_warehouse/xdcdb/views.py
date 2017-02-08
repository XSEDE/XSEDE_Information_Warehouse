from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from xdcdb.models import *
from xdcdb.serializers import *

# Create your views here.
class XcdbResource_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = TGResource.objects.all()
        serializer = XcdbResource_Serializer(objects, many=True)
        return Response(serializer.data)

class XcdbResource_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = TGResource.objects.get(pk=self.kwargs['id'])
            except Endpoint.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = XcdbResource_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = TGResource.objects.filter(info_resourceid__exact=self.kwargs['resourceid'])
            serializer = XcdbResource_Serializer(objects, many=True)
        return Response(serializer.data)

class XcdbResourcePublished_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get (self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object=TGResource.objects.get(pk=self.kwargs['id'])
            except TGResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = XcdbResourcePublished_Serializer(object)
        return Response(serializer.data)
