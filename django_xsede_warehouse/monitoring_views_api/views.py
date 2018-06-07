from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from monitoring_views_api.serializers import *

# Create your views here.
class Software_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'resourceid' in self.kwargs:
            try:
                objects = TestResult.objects.filter(ResourceID__exact=self.kwargs['resourceid'],IsSoftware=True)
            except TestResult.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND);
        else:
            try:
                objects = TestResult.objects.filter(IsSoftware=True)
            except TestResult.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND);
        try:
            sort_by = request.GET.get('sort')
            sorted_objects = objects.order_by(sort_by)
        except:
            sorted_objects = objects
        returnformat = request.query_params.get('format', 'json')
        if returnformat != 'html':
            serializer = TestResult_Serializer(sorted_objects, many=True)
            return Response(serializer.data)
        else:
            serializer = TestResult_DetailURL_Serializer(sorted_objects, context={'request': request, 'detail_url_name': 'software-status-detail'}, many=True)
            return render(request, 'monitoring_views_api/list.html', {'record_list': serializer.data})

class Service_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'resourceid' in self.kwargs:
            try:
                objects = TestResult.objects.filter(ResourceID__exact=self.kwargs['resourceid'],IsService=True)
            except TestResult.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND);
        else:
            try:
                objects = TestResult.objects.filter(IsService=True)
            except TestResult.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND);
        try:
            sort_by = request.GET.get('sort')
            sorted_objects = objects.order_by(sort_by)
        except:
            sorted_objects = objects
        returnformat = request.query_params.get('format', 'json')
        if returnformat != 'html':
            serializer = TestResult_Serializer(sorted_objects, many=True)
            return Response(serializer.data)
        else:
            serializer = TestResult_DetailURL_Serializer(sorted_objects, context={'request': request, 'detail_url_name': 'services-status-detail'}, many=True)
            return render(request, 'monitoring_views_api/list.html', {'record_list': serializer.data})

class Software_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        serializer = None
        if 'id' in self.kwargs:
            try:
                object = TestResult.objects.get(pk=uri_to_iri(self.kwargs['id']),IsSoftware=True) # uri_to_iri translates %xx
            except TestResult.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if returnformat != 'html':
                serializer = TestResult_Serializer(object)
                return Response(serializer.data)
            else:
                return render(request, 'monitoring_views_api/detail.html', {'record_list': [object]})

class Service_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        serializer = None
        if 'id' in self.kwargs:
            try:
                object = TestResult.objects.get(pk=uri_to_iri(self.kwargs['id']),IsService=True) # uri_to_iri translates %xx
            except TestResult.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if returnformat != 'html':
                serializer = TestResult_Serializer(object)
                return Response(serializer.data)
            else:
                return render(request, 'monitoring_views_api/detail.html', {'record_list': [object]})
