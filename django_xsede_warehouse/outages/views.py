from django.shortcuts import render
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status

from outages.models import *
from outages.serializers import *

# Create your views here.
class Outages_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=Outages_DetailURL_Serializer)
    def get(self, request, format=None):
        returnformat = request.query_params.get('format', 'json')
        try:
            sort_by = request.GET.get('sort')
            objects = Outages.objects.all().order_by(sort_by)
        except:
            objects = Outages.objects.all()
        if returnformat != 'html':
            serializer = Outages_Serializer(objects, many=True)
            return Response(serializer.data)
        else:
            serializer = Outages_DetailURL_Serializer(objects, context={'request': request}, many=True)
            return render(request, 'outages/list.html', {'record_list': serializer.data})


class Outages_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=Outages_Serializer)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if 'id' in self.kwargs:
            try:
                object = Outages.objects.get(pk=self.kwargs['id'])
            except Outages.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'ResourceID' in self.kwargs:
            object = Outages.objects.filter(info_resourceid__exact=self.kwargs['ResourceID'])
        if returnformat != 'html':
            serializer = Outages_Serializer(object)
            return Response(serializer.data)
        else:
            return render(request, 'outages/detail.html', {'record_list': [object]})

class Outages_By_Resource(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=Outages_Serializer)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if 'ResourceID' in self.kwargs:
            try:
                try:
                    sort_by = request.GET.get('sort')
                    objects = Outages.objects.filter(ResourceID__exact=self.kwargs['ResourceID']).order_by(sort_by)
                except:
                    objects = Outages.objects.filter(ResourceID__exact=self.kwargs['ResourceID'])
            except Outages.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if returnformat != 'html':
            serializer = Outages_Serializer(objects, many=True)
            return Response(serializer.data)
        else:
            return render(request, 'outages/list.html', {'record_list': objects})


class Outages_Current(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=Outages_Serializer)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        try:
            now = timezone.now()
            try:
                sort_by = request.GET.get('sort')
                objects = Outages.objects.filter(OutageStart__lte=now,OutageEnd__gte=now).order_by(sort_by)
            except:
                objects = Outages.objects.filter(OutageStart__lte=now,OutageEnd__gte=now)
        except Outages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if returnformat != 'html':
            serializer = Outages_Serializer(objects, many=True)
            return Response(serializer.data)
        else:
            return render(request, 'outages/list.html', {'record_list': objects})

class Outages_Past(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=Outages_Serializer)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        try:
            now = timezone.now()
            try:
                sort_by = request.GET.get('sort')
                objects = Outages.objects.filter(OutageEnd__lte=now).order_by(sort_by)
            except:
                objects = Outages.objects.filter(OutageEnd__lte=now)
        except Outages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if returnformat != 'html':
            serializer = Outages_Serializer(objects, many=True)
            return Response(serializer.data)
        else:
            return render(request, 'outages/list.html', {'record_list': objects})


class Outages_Future(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=Outages_Serializer)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        try:
            now = timezone.now()
            try:
                sort_by = request.GET.get('sort')
                objects = Outages.objects.filter(OutageStart__gte=now).order_by(sort_by)
            except:
                objects = Outages.objects.filter(OutageStart__gte=now)
        except Outages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if returnformat != 'html':
            serializer = Outages_Serializer(objects, many=True)
            return Response(serializer.data)
        else:
            return render(request, 'outages/list.html', {'record_list': objects})

class Outages_StatusRelevant(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(responses=Outages_Serializer)
    def get(self, request, format=None, **kwargs):
        now = timezone.now()
        returnformat = request.query_params.get('format', 'json')
        # Relevant means active in the last week into the future
        relevant_start = now - timezone.timedelta(days=7)
        if 'ResourceID' in self.kwargs:
            try:
                try:
                    sort_by = request.GET.get('sort')
                    objects = Outages.objects.filter(ResourceID__exact=self.kwargs['ResourceID'], OutageEnd__gte=relevant_start).order_by(sort_by)
                except:
                    objects = Outages.objects.filter(ResourceID__exact=self.kwargs['ResourceID'], OutageEnd__gte=relevant_start)
            except Outages.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if returnformat != 'html':
            serializer = Outages_Serializer(objects, many=True)
            return Response(serializer.data)
        else:
            return render(request, 'outages/list.html', {'record_list': objects})
