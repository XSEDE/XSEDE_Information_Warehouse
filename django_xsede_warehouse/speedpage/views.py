from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from speedpage.models import *
from speedpage.serializers import *

# Create your views here.
class speedpage_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=speedpage_Serializer)
    def get(self, request, format=None):
        objects = speedpage.objects.all()
        serializer = speedpage_Serializer(objects, many=True)
        return Response(serializer.data)

class speedpage_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=speedpage_Serializer)
    def get(self, request, format=None, **kwargs):
        if 'sourceid' in self.kwargs:
            if 'destid' in self.kwargs:
                try:
                    objects = speedpage.objects.filter(sourceid__exact=self.kwargs['sourceid'],destid__exact=self.kwargs['destid'])
                except speedpage.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    objects = speedpage.objects.filter(sourceid__exact=self.kwargs['sourceid'])
                except speedpage.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'destid' in self.kwargs:
            objects = speedpage.objects.filter(destid__exact=self.kwargs['destid'])
        serializer = speedpage_Serializer(objects, many=True)
        return Response(serializer.data)
