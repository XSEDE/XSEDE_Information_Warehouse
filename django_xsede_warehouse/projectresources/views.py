from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from projectresources.models import *
from projectresources.serializers import *

# Create your views here.
class ProjectResource_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=ProjectResource_Serializer)
    def get(self, request, format=None):
        objects = ProjectResource.objects.all()
        serializer = ProjectResource_Serializer(objects, many=True)
        return Response(serializer.data)

class ProjectResource_By_Resource(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=ProjectResource_Serializer)
    def get(self, request, format=None, **kwargs):
        if 'ResourceID' in self.kwargs:
            try:
                objects = ProjectResource.objects.filter(ResourceID__exact=self.kwargs['ResourceID'])
            except ProjectResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProjectResource_Serializer(objects, many=True)
        return Response(serializer.data)

class ProjectResource_By_Number(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=ProjectResource_Serializer)
    def get(self, request, format=None, **kwargs):
        if 'project_number' in self.kwargs:
            try:
                objects = ProjectResource.objects.filter(project_number=self.kwargs['project_number'])
            except ProjectResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProjectResource_Serializer(objects, many=True)
        return Response(serializer.data)
