from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from glue2_db.models import ApplicationEnvironment, AbstractService, ComputingActivity, ComputingQueue, Endpoint
from glue2_db.serializers import ComputingActivity_DbSerializer
from glue2_views_api.serializers import *
from xsede_warehouse.responses import MyAPIResponse
from xsede_warehouse.exceptions import MyAPIException
from xdcdb.models import XSEDELocalUsermap
from social_django.utils import psa

from mp_auth.backends.mp import GlobusAuthentication

import requests


# Create your views here.
class ApplicationEnvironment_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ApplicationEnvironment.objects.all()
        serializer = ApplicationEnvironment_Serializer(objects, many=True)
        return Response(serializer.data)

# Software information comes from ApplicationHandle and the related ApplicationEnvironment
class Software_List(APIView):
    '''
        GLUE2 software combining ApplicationEnvironment and AppliactionHandle
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ApplicationHandle.objects.all()
        serializer = ApplicationHandle_Serializer(objects, many=True)
        return Response(serializer.data)

class Software_Detail(APIView):
    '''
        GLUE2 software combining ApplicationEnvironment and AppliactionHandle
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = ApplicationHandle.objects.get(pk=uri_to_iri(self.kwargs['id'])) # uri_to_iri translates %xx
            except ApplicationHandle.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ApplicationHandle_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            serializer = ApplicationHandle_Serializer(objects, many=True)
        elif 'appname' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ApplicationEnvironment__AppName__exact=uri_to_iri(self.kwargs['appname']))
            serializer = ApplicationHandle_Serializer(objects, many=True)
        return Response(serializer.data)

# Service information comes from Endpoint and the parent AbstractService
class Services_List(APIView):
    '''
        GLUE2 services combining AbstractService and Endpoint
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = Endpoint.objects.all()
        serializer = EndpointServices_Support_Serializer(objects, many=True)
        return Response(serializer.data)

class Services_Detail(APIView):
    '''
        GLUE2 services combining AbstractService and Endpoint
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = Endpoint.objects.get(pk=self.kwargs['id'])
            except Endpoint.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = EndpointServices_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = Endpoint.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            serializer = EndpointServices_Serializer(objects, many=True)
        elif 'interfacename' in self.kwargs:
            objects = Endpoint.objects.filter(InterfaceName__exact=self.kwargs['interfacename'])
            serializer = EndpointServices_Serializer(objects, many=True)
        elif 'servicetype' in self.kwargs:
            objects = Endpoint.objects.filter(AbstractService__ServiceType__exact=self.kwargs['servicetype'])
            serializer = EndpointServices_Serializer(objects, many=True)
        return Response(serializer.data)

class Jobqueue_List(APIView):
    '''
        GLUE2 Jobs Queue from ComputingQueue
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (GlobusAuthentication,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'resourceid' in self.kwargs:
            try:
                objects = ComputingQueue.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            except ComputingQueue.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ResourceID not found')
        else:
            objects = ComputingQueue.objects.all()
        try:
            sort_by = request.GET.get('sort')
        except:
            sort_by = None
        serializer = ComputingQueue_Expand_Serializer(objects, many=True, context={'sort_by': sort_by})
        return MyAPIResponse({'result_set': serializer.data}, template_name='glue2_views_api/jobqueues.html')

class Job_Detail(APIView):
    '''
        GLUE2 Job Detail from ComputingActivity
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (GlobusAuthentication,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = ComputingActivity.objects.get(pk=self.kwargs['id'])
            except ComputingActivity.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ID not found')
        else:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='Invalid request')
        serializer = ComputingActivity_Expand_Serializer(object)
        return MyAPIResponse({'result_set': [serializer.data]}, template_name='glue2_views_api/job_detail.html')

class Job_List(APIView):
    '''
        GLUE2 Jobs from ComputingActivity
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (GlobusAuthentication,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                objects = [ComputingActivity.objects.get(pk=self.kwargs['id'])]
            except ComputingActivity.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ID not found')
        elif 'resourceid' in self.kwargs and 'queue' in self.kwargs:
            try:
                objects = ComputingActivity.objects.filter(ResourceID__exact=self.kwargs['resourceid']).filter(EntityJSON__Queue__exact=self.kwargs['queue'])
            except ComputingActivity.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ResourceID and Queue not found')
        elif 'resourceid' in self.kwargs and 'localaccount' in self.kwargs:
            try:
                objects = ComputingActivity.objects.filter(ResourceID__exact=self.kwargs['resourceid']).filter(EntityJSON__LocalOwner__exact=self.kwargs['localaccount'])
            except ComputingActivity.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ResourceID and LocalAccount not found')
        elif 'resourceid' in self.kwargs:
            try:
                objects = ComputingActivity.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            except ComputingActivity.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ResourceID not found')
        else:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='Invalid request')
        serializer = ComputingActivity_Expand_Serializer(objects, many=True, context={'request': request})
        return MyAPIResponse({'result_set': serializer.data}, template_name='glue2_views_api/jobs.html')

class Jobs_per_Resource_by_ProfileID(APIView):
    '''
        GLUE2 Jobs from ComputingActivity
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (GlobusAuthentication,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        import requests
        fullusername = None
        username = None
        if request.user.is_authenticated:
            fullusername = request.user.username
            username = fullusername[:fullusername.rfind("@")]

        if 'resourceid' in self.kwargs:
            try:
                localaccount = XSEDELocalUsermap.objects.get(ResourceID=self.kwargs['resourceid'],portal_login=username)
            except XSEDELocalUsermap.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='User not found in user database')
            try:
                    objects = ComputingActivity.objects.filter(ResourceID__exact=self.kwargs['resourceid']).filter(EntityJSON__LocalOwner__exact=localaccount.local_username)
            except ComputingActivity.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ResourceID and LocalAccount not found')
        else:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='Invalid request')
        serializer = ComputingActivity_Expand_Serializer(objects, many=True, context={'request': request})
        return MyAPIResponse({'result_set': serializer.data}, template_name='glue2_views_api/jobs.html')

class Jobs_by_ProfileID(APIView):
    '''
        GLUE2 Jobs from ComputingActivity
    '''
    authentication_classes = (GlobusAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        import requests
        fullusername = None
        username = None
        if request.user.is_authenticated:
            fullusername = request.user.username
            username = fullusername[:fullusername.rfind("@")]

            try:
                localaccounts = XSEDELocalUsermap.objects.filter(portal_login=username)
            except XSEDELocalUsermap.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='User not found in user database')
            localusernames = []
            resourceusers = {}
            for account in localaccounts:
                localuser = account.local_username
                localusernames.append(localuser)
                resourceusers[account.ResourceID+localuser] = True
            try:
                    objects = ComputingActivity.objects.filter(EntityJSON__LocalOwner__in=localusernames)
            except ComputingActivity.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ResourceID and LocalAccount not found')
            jobstoreturn = []
            for job in objects:
                if resourceusers.get(job.ResourceID+job.EntityJSON['LocalOwner'], False):
                    jobstoreturn.append(job)
        else:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='Invalid request')
        serializer = ComputingActivity_Expand_Serializer(jobstoreturn, many=True, context={'request': request})
        return MyAPIResponse({'result_set': serializer.data}, template_name='glue2_views_api/jobs.html')
