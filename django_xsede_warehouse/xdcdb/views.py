from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer

from xdcdb.models import *
from xdcdb.serializers import *
from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse

# Create your views here.
class XSEDEResource_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        try:
            sort_by = request.GET.get('sort')
            objects = TGResource.objects.all().order_by(sort_by)
        except:
            objects = TGResource.objects.all()
        serializer = XSEDEResource_DetailURL_Serializer(objects, context={'request': request}, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='xdcdb/resource_list.html')

class XSEDEResource_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if 'id' in self.kwargs:
            try:
                objects = [TGResource.objects.get(pk=self.kwargs['id'])]
            except TGResource.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Resource ID not found')
        elif 'resourceid' in self.kwargs:
            try:
                objects = TGResource.objects.filter(info_resourceid__exact=self.kwargs['resourceid'])
            except TGResource.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Resource ID not found')
        serializer = XSEDEResource_Serializer(objects, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='xdcdb/resource_detail.html')

class XSEDEResourcePublished_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get (self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                objects = [TGResource.objects.get(pk=self.kwargs['id'])]
            except TGResource.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Resource ID not found')
            serializer = XSEDEResourcePublished_Serializer(objects, many=True)
            response_obj = {'results': serializer.data}
            return MyAPIResponse(response_obj, template_name='xdcdb/resource_detail.html')

class XSEDEPerson_Detail(APIView):
    '''
        ### Person detail
        
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
    '''
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                objects = [XSEDEPerson.objects.get(pk=self.kwargs['id'])]
            except XSEDEPerson.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Person ID not found')
        elif 'portalid' in self.kwargs:
            try:
                objects = XSEDEPerson.objects.filter(portal_login__exact=self.kwargs['portalid'])
            except XSEDEPerson.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Portal ID not found')
            if len(objects) > 1:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Unexpected multiple Portal ID found')
        serializer = XSEDEPerson_Serializer(objects, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='xdcdb/person_detail.html')

class XSEDEPerson_Search(APIView):
    '''
        ### Person search the Portal ID, Last Name, First Name, and e-mail addresses fields
        
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
    '''
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        sort_by = request.GET.get('sort', 'portal_login')
        search_strings = kwargs.get('search_strings', request.GET.get('search_strings', None))
        if search_strings is None or search_strings == '':
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Search string missing')
        
        try:
            objects = XSEDEPerson.objects.filter( Q(portal_login__contains=search_strings) | Q(last_name__contains=search_strings) | Q(first_name__contains=search_strings) | Q(emails__contains=search_strings) ).order_by(sort_by)
        except XSEDEPerson.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='No persons match search string')
        serializer = XSEDEPerson_Serializer(objects, context={'request': request}, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='xdcdb/person_list.html')

