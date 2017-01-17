from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status

from processing_status.models import *
from processing_status.serializers import *

# Create your views here.
class ProcessingRecord_DbList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ProcessingRecord.objects.all()
        serializer = ProcessingRecord_DbSerializer(objects, many=True)
        return Response(serializer.data)
