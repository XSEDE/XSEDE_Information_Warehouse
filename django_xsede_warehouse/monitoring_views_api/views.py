from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from serializers import *
import pdb

# Create your views here.
class Software_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        # objects = TestResult.objects.all()
        objects = TestResult.objects.filter(IsSoftware=True)
        serializer = TestResult_Serializer(objects, many=True)
        return Response(serializer.data)

class Service_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        # objects = TestResult.objects.all()
        objects = TestResult.objects.filter(IsService=True)
        serializer = TestResult_Serializer(objects, many=True)
        return Response(serializer.data)

class Software_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        serializer = None
        if 'id' in self.kwargs:
            try:
                object = TestResult.objects.get(pk=uri_to_iri(self.kwargs['id']),IsSoftware=True) # uri_to_iri translates %xx
            except TestResult.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = TestResult_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = TestResult.objects.filter(ResourceID__exact=self.kwargs['resourceid'],IsSoftware=True)
            serializer = TestResult_Serializer(objects, many=True)
        return Response(serializer.data)

class Service_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        serializer = None
        if 'id' in self.kwargs:
            try:
                object = TestResult.objects.get(pk=uri_to_iri(self.kwargs['id']),IsService=True) # uri_to_iri translates %xx
            except TestResult.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = TestResult_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = TestResult.objects.filter(ResourceID__exact=self.kwargs['resourceid'],IsService=True)
            serializer = TestResult_Serializer(objects, many=True)
        return Response(serializer.data)