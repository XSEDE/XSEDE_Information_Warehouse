from django.http import *
from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from django.utils.dateparse import parse_datetime

# Create your views here.
from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from glue2_db.models import *
from glue2_db.serializers import *

from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse

import pytz
UTC = pytz.timezone("UTC")

#from django.core.urlresolvers import resolve
import logging
logg2 = logging.getLogger('xsede.glue2')

#class ApplicationEnvironmentSet(viewsets.ReadOnlyModelViewSet):
#    queryset = ApplicationEnvironment.objects.all()
#    serializer_class = ApplicationEnvironment_DbSerializer

class ApplicationEnvironment_DbList(APIView):
    '''
        GLUE2 Application Environment entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ApplicationEnvironment.objects.all()
        serializer = ApplicationEnvironment_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ApplicationEnvironment_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationEnvironment_DbDetail(APIView):
    '''
        GLUE2 Application Environment entity
    '''
    # Since Name, AppVersion, and ID may contain a forward slash we use uri_to_iri
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = ApplicationEnvironment.objects.get(pk=uri_to_iri(pk)) # uri_to_iri translates %xx
        except ApplicationEnvironment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ApplicationEnvironment_DbSerializer(object).data)
    def put(self, request, pk, format=None):
        try:
            object = ApplicationEnvironment.objects.get(pk=uri_to_iri(pk))
        except ApplicationEnvironment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationEnvironment_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = ApplicationEnvironment.objects.get(pk=uri_to_iri(pk))
        except ApplicationEnvironment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ApplicationHandle_DbList(APIView):
    '''
        GLUE2 Application Handle entity
    '''
    # Since Name, Value, and ID may contain a forward slash we use uri_to_iri
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ApplicationHandle.objects.all()
#        serializer = ApplicationHandle_DbSerializer(objects, many=True, context={'request', request})
        serializer = ApplicationHandle_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ApplicationHandle_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationHandle_DbDetail(APIView):
    '''
        GLUE2 Application Handle entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = ApplicationHandle.objects.get(pk=uri_to_iri(pk))
        except ApplicationHandle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
#        serializer = ApplicationHandle_DbSerializer(object, context={'request', request})
        return Response(ApplicationHandle_DbSerializer(object).data)
    def put(self, request, pk, format=None):
        try:
            object = ApplicationHandle.objects.get(pk=uri_to_iri(pk))
        except ApplicationHandle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationHandle_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = ApplicationHandle.objects.get(pk=uri_to_iri(pk))
        except ApplicationHandle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AbstractService_DbList(APIView):
    '''
        GLUE2 Abstract Service entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = AbstractService.objects.all()
        serializer = AbstractService_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = AbstractService_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AbstractService_DbDetail(APIView):
    '''
        GLUE2 Abstract Service entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = AbstractService.objects.get(pk=pk)
        except AbstractService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AbstractService_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = AbstractService.objects.get(pk=pk)
        except AbstractService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AbstractService_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = AbstractService.objects.get(pk=pk)
        except AbstractService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Endpoint_DbList(APIView):
    '''
        GLUE2 Endpoint entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = Endpoint.objects.all()
        serializer = Endpoint_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = Endpoint_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Endpoint_DbDetail(APIView):
    '''
        GLUE2 Endpoint entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = Endpoint.objects.get(pk=pk)
        except Endpoint.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Endpoint_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = Endpoint.objects.get(pk=pk)
        except Endpoint.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Endpoint_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = Endpoint.objects.get(pk=pk)
        except Endpoint.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ComputingManager_DbList(APIView):
    '''
        GLUE2 Computing Manager entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ComputingManager.objects.all()
        serializer = ComputingManager_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ComputingManager_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComputingManager_DbDetail(APIView):
    '''
        GLUE2 Computing Manager entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = ComputingManager.objects.get(pk=pk)
        except ComputingManager.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingManager_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = ComputingManager.objects.get(pk=pk)
        except ComputingManager.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingManager_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = ComputingManager.objects.get(pk=pk)
        except ComputingManager.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExecutionEnvironment_DbList(APIView):
    '''
        GLUE2 Execution Environment entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ExecutionEnvironment.objects.all()
        serializer = ExecutionEnvironment_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ExecutionEnvironment_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExecutionEnvironment_DbDetail(APIView):
    '''
        GLUE2 Execution Environment entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = ExecutionEnvironment.objects.get(pk=pk)
        except ExecutionEnvironment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExecutionEnvironment_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = ExecutionEnvironment.objects.get(pk=pk)
        except ExecutionEnvironment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExecutionEnvironment_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = ExecutionEnvironment.objects.get(pk=pk)
        except ExecutionEnvironment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Location_DbList(APIView):
    '''
        GLUE2 Location entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = Location.objects.all()
        serializer = Location_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = Location_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Location_DbDetail(APIView):
    '''
        GLUE2 Location entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Location_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Location_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ComputingShare_DbList(APIView):
    '''
        GLUE2 Computing Share entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ComputingShare.objects.all()
        serializer = ComputingShare_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ComputingShare_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComputingShare_DbDetail(APIView):
    '''
        GLUE2 Computing Share entity
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        try:
            object = ComputingShare.objects.get(pk=pk)
        except ComputingShare.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingShare_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = ComputingShare.objects.get(pk=pk)
        except ComputingShare.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingShare_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = ComputingShare.objects.get(pk=pk)
        except ComputingShare.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ComputingQueue_DbList(APIView):
    '''
        GLUE2 Computing Queue entity
    '''
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None, **kwargs):
        if 'resourceid' in self.kwargs:
            try:
                objects = ComputingQueue.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            except ComputingQueue.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                objects = ComputingQueue.objects.all()
            except ComputingQueue.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingQueue_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ComputingQueue_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComputingQueue_DbDetail(APIView):
    '''
        GLUE2 Computing Queue entity
    '''
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        try:
            object = ComputingQueue.objects.get(pk=pk)
        except ComputingQueue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingQueue_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = ComputingQueue.objects.get(pk=pk)
        except ComputingQueue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingQueue_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = ComputingQueue.objects.get(pk=pk)
        except ComputingQueue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ComputingActivity_DbList(APIView):
    '''
        GLUE2 Computing Activity entity
    '''
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        objects = ComputingActivity.objects.all()
        serializer = ComputingActivity_DbSerializer(objects, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ComputingActivity_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComputingActivity_DbDetail(APIView):
    '''
        GLUE2 Computing Activity entity
    '''
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        try:
            object = ComputingActivity.objects.get(pk=pk)
        except ComputingActivity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingActivity_DbSerializer(object)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            object = ComputingActivity.objects.get(pk=pk)
        except ComputingActivity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ComputingActivity_DbSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            object = ComputingActivity.objects.get(pk=pk)
        except ComputingActivity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EntityHistory_DbList(APIView):
    '''
        ### GLUE2 entityhistory search and list
        
        Optional selection argument(s):
        ```
            start_date=<yyyy-mm-dd>
            end_date=<yyyy-mm-dd>
            resourceid=<resourceid>
        ```
        Optional response argument(s):
        ```
            fields=__usage__                    (return three fields for usage analysis)
            format={json,xml,html}              (json default)
        ```
        .
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'doctype' not in self.kwargs:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Missing /doctype/.. argument')
        arg_doctype = kwargs['doctype']
        
        try:
            dt = request.GET.get('start_date', None)
            pdt = parse_datetime(dt)
            if pdt is None: # If it was only a date try adding the time
                pdt = parse_datetime(dt + 'T00:00:00.0+00:00')
            if pdt is None:
                raise Exception
            arg_startdate = pdt.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
        except:
            arg_startdate = None
        
        try:
            dt = request.GET.get('end_date', None)
            pdt = parse_datetime(dt)
            if pdt is None: # If it was only a date try adding the time
                pdt = parse_datetime(dt + 'T23:59:59.0+00:00')
            if pdt is None:
                raise Exception
            arg_enddate = (pdt.astimezone(UTC) + timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%S%z')
        except:
            arg_enddate = None

        arg_resourceid = request.GET.get('resourceid', None)

        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        objects = EntityHistory.objects.filter(DocumentType=arg_doctype)

        if arg_resourceid:
            objects = objects.filter(ResourceID=arg_resourceid)             # String Comparison
        if arg_startdate:
            objects = objects.filter(ReceivedTime__gte=arg_startdate)       # String Comparison
        if arg_enddate:
            objects = objects.filter(ReceivedTime__lt=arg_enddate)         # String Comparison

        if '__usage__' in want_fields:
            serializer = EntityHistory_Usage_Serializer(objects, many=True)
        else:
            serializer = EntityHistory_DbSerializer(objects, many=True)
        response_obj = {'results': serializer.data}
        response_obj['total_results'] = len(objects)
        return MyAPIResponse(response_obj)
    
    def post(self, request, format=None):
        serializer = EntityHistory_DbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EntityHistory_DbDetail(APIView):
    '''
        GLUE2 received entity history
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, id, format=None):
        try:
            object = EntityHistory.objects.get(pk=id)
        except EntityHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EntityHistory_DbSerializer(object)
        return Response(serializer.data)
