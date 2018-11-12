import csv
from django.http import HttpResponse

from django.utils.encoding import uri_to_iri
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework import status

from rdr_db.models import RDRResource
from rdr_db.filters import *
from resource_status_api.serializers import *

from processing_status.models import *
from processing_status.serializers import *

from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse

# Create your views here.
class ProcessingRecord_DbList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'about' in self.kwargs:
            try:
                objects = ProcessingRecord.objects.filter(About__exact=uri_to_iri(self.kwargs['about']))
            except ProcessingRecord.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified about not found')
        elif 'topic' in self.kwargs:
            try:
                objects = ProcessingRecord.objects.filter(Topic__exact=uri_to_iri(self.kwargs['topic']))
            except ProcessingRecord.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified topic not found')
        else:
            try:
                objects = ProcessingRecord.objects.all()
            except ProcessingRecord.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='No objects found')
        try:
            sort_by = request.GET.get('sort')
            objects_sorted = objects.order_by(sort_by)
        except:
            objects_sorted = objects
        serializer = ProcessingRecord_DetailURL_DbSerializer(objects_sorted, context={'request': request}, many=True)
        return MyAPIResponse({'record_list': serializer.data}, template_name='processing_status/list.html')

class ProcessingRecord_LatestList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'about' in self.kwargs:
            try:
                object = ProcessingRecord.objects.filter(About__exact=uri_to_iri(self.kwargs['about'])).latest('ProcessingStart')
            except ProcessingRecord.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified about not found')
        elif 'topic' in self.kwargs:
            try:
                object = ProcessingRecord.objects.filter(Topic__exact=uri_to_iri(self.kwargs['topic'])).latest('ProcessingStart')
            except ProcessingRecord.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified topic not found')
        else:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Not found')
        serializer = ProcessingRecord_DbSerializer(object)
        return MyAPIResponse({'record_list': [serializer.data]}, template_name='processing_status/detail.html')

class ProcessingRecord_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = ProcessingRecord.objects.get(pk=uri_to_iri(self.kwargs['id']))
            except ProcessingRecord.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified id not found')
        else:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Not found')
        if request.accepted_renderer.format == 'html':
            return MyAPIResponse({'record_list': [object]}, template_name='processing_status/detail.html')
        serializer = ProcessingRecord_DbSerializer(object)
        return MyAPIResponse({'record_list': [serializer.data]})

class PublisherInfo_DbList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'resourceid' in self.kwargs:
            try:
                objects = PublisherInfo.objects.filter(ResourceID__exact=uri_to_iri(self.kwargs['resourceid']))
            except PublisherInfo.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified ResourceID not found')
        else:
            try:
                objects = PublisherInfo.objects.all()
            except PublisherInfo.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='No objects found')
        try:
            sort_by = request.GET.get('sort')
            objects_sorted = objects.order_by(sort_by)
        except:
            objects_sorted = objects

        serializer = PublisherInfo_DetailURL_DbSerializer(objects_sorted, context={'request': request}, many=True)
        return MyAPIResponse({'record_list': serializer.data}, template_name='processing_status/publisher_list.html')

class PublisherInfo_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = PublisherInfo.objects.get(pk=uri_to_iri(self.kwargs['id']))
            except PublisherInfo.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ID parameter is not valid')
        else:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ID not found')

        if request.accepted_renderer.format == 'html':
            return MyAPIResponse({'record_list': [object]}, template_name='processing_status/publisher_detail.html')
        serializer = PublisherInfo_DbSerializer(object)
        return MyAPIResponse({'record_list': [serializer.data]})
