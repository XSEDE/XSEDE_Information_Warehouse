from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from xdcdb.models import *
from xdcdb.serializers import *

# Create your views here.
class XcdbResource_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        try:
            sort_by = request.GET.get('sort')
            objects = TGResource.objects.all().order_by(sort_by)
        except:
            objects = TGResource.objects.all()
        returnformat = request.query_params.get('format', 'json')
        if returnformat != 'html':
            serializer = XcdbResource_Serializer(objects, many=True)
            return Response(serializer.data)
        else:
            serializer = XcdbResource_DetailURL_Serializer(objects, context={'request': request}, many=True)
            return render(request, 'xdcdb/list.html', {'resource_list': serializer.data})

class XcdbResource_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if 'id' in self.kwargs:
            try:
                object = TGResource.objects.get(pk=self.kwargs['id'])
            except Endpoint.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = XcdbResource_Serializer(object)
            if returnformat != 'html':
                return Response(serializer.data)
            else:
                return render(request, 'xdcdb/detail.html', {'resource_list': [object]})
        elif 'resourceid' in self.kwargs:
            objects = TGResource.objects.filter(info_resourceid__exact=self.kwargs['resourceid'])
            serializer = XcdbResource_Serializer(objects, many=True)
            if returnformat != 'html':
                return Response(serializer.data)
            else:
                return render(request, 'xdcdb/detail.html', {'resource_list': serializer.data})

class XcdbResourcePublished_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get (self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if 'id' in self.kwargs:
            try:
                object = TGResource.objects.get(pk=self.kwargs['id'])
            except Endpoint.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = XcdbResourcePublished_Serializer(object)
            if returnformat != 'html':
                return Response(serializer.data)
            else:
                return render(request, 'xdcdb/detail.html', {'resource_list': [object]})
