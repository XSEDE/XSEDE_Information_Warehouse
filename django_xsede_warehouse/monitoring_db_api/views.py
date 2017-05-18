from __future__ import print_function
from django.http import *
from django.shortcuts import render
from django.utils.encoding import uri_to_iri

# Create your views here.
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from monitoring_db.models import *
from monitoring_db.serializers import *

import logging
logg2 = logging.getLogger('xsede.glue2')

class TestResult_DbList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = TestResult.objects.all()
        serializer = TestResult_DbSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TestResult_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestResult_DbDetail_Source(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        path_info = request.META.get('PATH_INFO',None)
        serializer = None
        if 'inca' in path_info:
            objects = TestResult.objects.filter(Source__exact='inca')
            serializer = TestResult_DbSerializer(objects, many=True)
        elif 'nagios' in path_info:
            objects = TestResult.objects.filter(Source__exact='nagios')
            serializer = TestResult_DbSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        path_info = request.META.get('PATH_INFO', None)
        if 'inca' or 'nagios' in path_info:
            serializer = TestResult_DbSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestResult_DbDetail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = TestResult.objects.get(pk=pk)
        except TestResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TestResult_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = TestResult.objects.get(pk=pk)
        except TestResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TestResult_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = TestResult.objects.get(pk=pk)
        except TestResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
