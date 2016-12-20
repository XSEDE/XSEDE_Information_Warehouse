from django.db.models import Q
from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
#from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rdr_db.models import RDRResource
from rdr_db.filters import *
from monitoring_db.models import TestResult
from resource_status_api.serializers import *
import pdb

# Create your views here.

class Resource_Status_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        #Note:  the query_param 'format' is used for magical things 
        #If we use it, it will work fine for json or html, but won't 
        #let us accept a random string as 'format' and still return json

        if 'resourceid' in self.kwargs:
            try:
                objects = RDRResource.objects.filter(info_resourceid__exact=uri_to_iri(self.kwargs['resourceid'])).filter(rdr_type__in=['compute','storage'])
            except RDRResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            objects = RDR_Active_Sub_Resources()
        serializer = Resource_Status_Serializer(objects, context={'request': request}, many=True)
        if returnformat != 'html':
            #Thought I was having a problem when not specifying a format at all
            #was getting OrderedDict returned in browser instead of json.
            #Turns out, that's django magic when hitting the REST endpoint 
            #from a browser.  The following two lines will make it always
            #really return JSON, but we're not doing that in other views...
            #returnresponse =  JSONRenderer().render(serializer.data)
            #return Response(returnresponse)
            return Response(serializer.data)
        else:
            return render(request, 'resources.html', {'resource_list': serializer.data})

#class Resource_Status_Detail(APIView):
#    permission_classes = (IsAuthenticatedOrReadOnly,)
#    def get(self, request, format=None, **kwargs):
#        if 'id' in self.kwargs:
#            try:
#                object = ApplicationHandle.objects.get(pk=uri_to_iri(self.kwargs['id'])) # uri_to_iri translates %xx
#            except ApplicationHandle.DoesNotExist:
#                return Response(status=status.HTTP_404_NOT_FOUND)
#            serializer = ApplicationHandle_Serializer(object)
#        elif 'resourceid' in self.kwargs:
#            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
#            serializer = ApplicationHandle_Serializer(objects, many=True)
#        elif 'appname' in self.kwargs:
#            objects = ApplicationHandle.objects.filter(ApplicationEnvironment__AppName__exact=uri_to_iri(self.kwargs['appname']))
#            serializer = ApplicationHandle_Serializer(objects, many=True)
#        return Response(serializer.data)
