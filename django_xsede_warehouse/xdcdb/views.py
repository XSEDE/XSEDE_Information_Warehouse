from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from mp_auth.backends.mp import GlobusAuthentication

from xdcdb.models import *
from xdcdb.serializers import *
from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse

# Create your views here.
class XSEDEResource_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    @extend_schema(responses=XSEDEResource_DetailURL_Serializer)
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
    @extend_schema(responses=XSEDEResource_Serializer)
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
    @extend_schema(responses=XSEDEResourcePublished_Serializer)
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
    authentication_classes = (GlobusAuthentication,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    @extend_schema(responses=XSEDEPerson_Serializer)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                objects = [XSEDEPerson.objects.get(pk=self.kwargs['id'])]
            except XSEDEPerson.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Person ID not found')
            except ValueError:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Person ID is not valid')
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
        ### Person search
        * Searches for case insensitive string(s) in fields
        * Fields: Portal ID, Last Name, First Name, and e-mail addresses
        * If multiple space delimited strings are specific, the 'match' argument determines whether any (default) or all strings must match
        
        Optional response argument(s):
        ```
            match={any,all}
            format={json,xml,html}              (json default)
        ```
    '''
#    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (GlobusAuthentication,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    @extend_schema(responses=XSEDEPerson_Serializer)
    def get(self, request, format=None, **kwargs):
        search_strings = kwargs.get('search_strings', request.GET.get('search_strings', None))
        if search_strings is None or search_strings == '':
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Search string missing')
        sort_by = request.GET.get('sort', 'portal_login')
        match_mode = request.GET.get('match', 'any').lower()
        if match_mode == 'and':
            match_mode = 'all'
        elif match_mode == 'or':
            match_mode = 'any'
        
        try:
            query = None
            for word in search_strings.split():
                if not query:
                    query = ( Q(portal_login__icontains=word) | Q(last_name__icontains=word) | Q(first_name__icontains=word) | Q(emails__icontains=word) )
                elif match_mode == 'all':
                    query = query & ( Q(portal_login__icontains=word) | Q(last_name__icontains=word) | Q(first_name__icontains=word) | Q(emails__icontains=word) )
                else:
                    query = query | ( Q(portal_login__icontains=word) | Q(last_name__icontains=word) | Q(first_name__icontains=word) | Q(emails__icontains=word) )
            objects = XSEDEPerson.objects.filter( query ).order_by(sort_by)
        except XSEDEPerson.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='No persons match search string')
        serializer = XSEDEPerson_Serializer(objects, context={'request': request}, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='xdcdb/person_list.html')

class XSEDEFos_List(APIView):
    '''
        ### Field of Science list
        
        Optional selection argument(s):
        ```
            search_strings=<comma_delimited_search_strings>
        ```
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
            sort=<field>                        (disables hierarchy=true)
            hierarchy=true                      (in html output display hierarchy)
            inactive=true                       (don't return only active)
        ```
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    @extend_schema(responses=XSEDEFos_DetailURL_Serializer)
    def get(self, request, format=None, **kwargs):
        arg_strings = request.GET.get('search_strings', None)
        if arg_strings:
            want_strings = list(arg_strings.replace(',', ' ').lower().split())
        else:
            want_strings = list()

        arg_hierarchy = request.GET.get('hierarchy', None)
        if arg_hierarchy and arg_hierarchy != '':
            want_hierarchy = True
        else:
            want_hierarchy = False

        arg_inactive = request.GET.get('inactive', None)
        if arg_inactive and arg_inactive != '':
            want_inactive = True
        else:
            want_inactive = False

        if 'parentid' in self.kwargs:
            try:
                objects = XSEDEFos.objects.filter(parent_field_of_science_id__exact=self.kwargs['parentid'])
            except XSEDEFos.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Parent ID not found')
        elif want_strings:
            try:
                objects = XSEDEFos.objects.filter(field_of_science_desc__icontains=want_strings[0])
                for another in want_strings[1:]:
                    objects = objects.filter(field_of_science_desc__icontains=another)
            except:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Unexpected error handling search_strings')
        else:
            try:
                objects = XSEDEFos.objects.all()
            except:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Fields of Science not found')
        if not want_inactive:
            objects = objects.filter(is_active=True)

        sort_by = request.GET.get('sort')
        if sort_by:
            objects = objects.order_by(sort_by)

        serializer = XSEDEFos_DetailURL_Serializer(objects, context={'request': request}, many=True)

        reqformat = format or request.GET.get('format', None)
        if reqformat == 'xml' or reqformat == 'json' or sort_by or not want_hierarchy:
            response_obj = {'results': serializer.data}
            return MyAPIResponse(response_obj, template_name='xdcdb/fos_list.html')

        if not sort_by and want_hierarchy:
            # 1. Create description and parent lookup dictionaries
            desc_lookup = {}
            parent_lookup = {}
            for item in serializer.data:
                desc_lookup[item['field_of_science_id']] = item['field_of_science_desc']
                parent_lookup[item['field_of_science_id']] = item['parent_field_of_science_id']
            # 2. Create sort and depth lookup maps
            sort_map = {}   # The textual field we will sort by
            depth_map = {}  # Distance to an item without a parent
            for item in serializer.data:
                self.build_sort_depth(item['field_of_science_id'], sort_map, depth_map, desc_lookup, parent_lookup)
        
        response_list = list()
        for item in serializer.data:
            response_item = dict(item)
            response_item['sort'] = sort_map[item['field_of_science_id']]
            if depth_map[item['field_of_science_id']] == 0:
                prefix = ''
            else:
                prefix = (depth_map[item['field_of_science_id']] * 4) * '&nbsp;'
            response_item['print_desc'] = prefix + item['field_of_science_desc']
            response_list.append(response_item)
            
        response_obj = {'results': sorted(response_list, key=lambda i: i['sort'])}
        return MyAPIResponse(response_obj, template_name='xdcdb/fos_list.html')

    def build_sort_depth(self, myid, sm, dm, dl, pl):
        if pl[myid] is None or pl[myid] == '':
            # I don't have a parent, use my own description, depth is 0
            sm[myid] = dl[myid]
            dm[myid] = 0
            return
        if pl[myid] not in sm:
            # My parent doesn't have an SL, iterate to get it
            self.build_sort_depth(pl[myid], sm, dm, dl, pl)
        # Append my parent SL with my own description, increment depth
        sm[myid] = sm[pl[myid]] + ':' + dl[myid]
        dm[myid] = dm[pl[myid]] + 1

class XSEDEFos_Detail(APIView):
    '''
        ### Field of Science detail
        
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    @extend_schema(responses=XSEDEFos_Serializer)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', 'json')
        if not 'id' in self.kwargs:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Missing ID argument')

        try:
            objects = [XSEDEFos.objects.get(pk=self.kwargs['id'])]
        except XSEDEFos.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified FOS ID not found')
        serializer = XSEDEFos_Serializer(objects, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='xdcdb/fos_detail.html')

