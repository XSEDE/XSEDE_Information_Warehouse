import csv
from django.http import HttpResponse

from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status

from rdr_db.models import RDRResource
from rdr_db.filters import *
from resource_status_api.serializers import *

from processing_status.models import *
from processing_status.serializers import *

# Create your views here.
class ProcessingRecord_DbList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if 'resourceid' in self.kwargs:
            try:
                try:
                    sort_by = request.GET.get('sort')
                    objects = ProcessingRecord.objects.filter(About__exact=uri_to_iri(self.kwargs['resourceid'])).order_by(sort_by)
                except:
                    objects = ProcessingRecord.objects.filter(About__exact=uri_to_iri(self.kwargs['resourceid']))
            except ProcessingRecord.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND);
        else:
            try:
                sort_by = request.GET.get('sort')
                objects = ProcessingRecord.objects.all().order_by(sort_by)
            except:
                objects = ProcessingRecord.objects.all()
        if returnformat != 'html':
            serializer = ProcessingRecord_DbSerializer(objects, many=True)
            return Response(serializer.data)
        else:
            return render(request, 'processing_status/list.html', {'record_list': objects})

class ProcessingRecord_LatestList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if 'about' in self.kwargs:
            try:
                object = ProcessingRecord.objects.filter(About__exact=uri_to_iri(self.kwargs['about'])).latest('ProcessingStart')
            except ProcessingRecord.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'topic' in self.kwargs:
            try:
                object = ProcessingRecord.objects.filter(Topic__exact=uri_to_iri(self.kwargs['topic'])).latest('ProcessingStart')
            except ProcessingRecord.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if returnformat != 'html':
            serializer = ProcessingRecord_DbSerializer(object)
            return Response(serializer.data)
        else:
            return render(request, 'processing_status/list.html', {'record_list': [object]})


class ProcessingRecord_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if 'id' in self.kwargs:
            try:
                object = ProcessingRecord.objects.get(pk=uri_to_iri(self.kwargs['id']))
            except ProcessingRecord.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if returnformat != 'html':
            serializer = ProcessingRecord_DbSerializer(object)
            return Response(serializer.data)
        else:
            return render(request, 'processing_status/detail.html', {'record_list': [object]})
