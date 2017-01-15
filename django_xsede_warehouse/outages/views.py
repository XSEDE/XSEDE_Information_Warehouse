from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from outages.models import *
from outages.serializers import *


# Create your views here.
class Outages_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = Outages.objects.all()
        serializer = Outages_Serializer(objects, many=True)
        return Response(serializer.data)

class Outages_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = Outages.objects.get(pk=self.kwargs['id'])
            except Outages.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = Outages_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = Outages.objects.filter(info_resourceid__exact=self.kwargs['resourceid'])
            serializer = Outages_Serializer(objects, many=True)
        return Response(serializer.data)

class Outages_By_Resource(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'ResourceID' in self.kwargs:
            try:
                objects = Outages.objects.filter(ResourceID__exact=self.kwargs['ResourceID'])
            except Outages.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = Outages_Serializer(objects, many=True)
        return Response(serializer.data)

class Outages_Current(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        try:
            now = timezone.now()
            objects = Outages.objects.filter(OutageStart__lte=now,OutageEnd__gte=now)
        except Outages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Outages_Serializer(objects, many=True)
        return Response(serializer.data)
class Outages_Past(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        try:
            now = timezone.now()
            objects = Outages.objects.filter(OutageEnd__lte=now)
        except Outages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Outages_Serializer(objects, many=True)
        return Response(serializer.data)

class Outages_Future(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        try:
            now = timezone.now()
            objects = Outages.objects.filter(OutageStart__gte=now)
        except Outages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Outages_Serializer(objects, many=True)
        return Response(serializer.data)

class Outages_StatusRelevant(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        now = timezone.now()
        # Relevant means active in the last week into the future
        relevant_start = now - timezone.timedelta(days=7)
        if 'ResourceID' in self.kwargs:
            try:
                objects = Outages.objects.filter(ResourceID__exact=self.kwargs['ResourceID'], OutageEnd__gte=relevant_start)
            except Outages.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = Outages_Serializer(objects, many=True)
        return Response(serializer.data)
