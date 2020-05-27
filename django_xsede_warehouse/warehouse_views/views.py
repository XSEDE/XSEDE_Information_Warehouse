from django.db.models import Q
from django.core.serializers import serialize
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.encoding import uri_to_iri
from django.urls import reverse, get_script_prefix

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework import status
from rdr_db.models import RDRResource
from rdr_db.filters import *
from glue2_db.models import ApplicationHandle
from xdcdb.models import *
from xdcdb.serializers import *
from rdr_db.serializers import *
from warehouse_views.serializers import Generic_Resource_Serializer, Software_Full_Serializer, Software_Community_Serializer
from xsede_warehouse.responses import MyAPIResponse

# Create your views here.
class RDR_List(APIView):
    '''
        ### RDR resource list
        
        Optional selection argument(s):
        ```
            info_siteid=<siteid>
        ```
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
            sort=<field>
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', None)
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='ALL', result='RESOURCEID')
        if 'info_siteid' in self.kwargs:
            try:
                sort_by = request.GET.get('sort')
                objects = RDRResource.objects.filter(rdr_type='resource').filter(info_siteid__exact=uri_to_iri(self.kwargs['info_siteid'])).order_by(sort_by)
            except:
                objects = RDRResource.objects.filter(rdr_type='resource').filter(info_siteid__exact=uri_to_iri(self.kwargs['info_siteid']))
        else:
            try:
                sort_by = request.GET.get('sort')
                objects = RDRResource.objects.filter(rdr_type='resource').order_by(sort_by)
            except:
                objects = RDRResource.objects.filter(rdr_type='resource').order_by('info_resourceid')
        for o in objects:
            o.Active = o.info_resourceid in active_resourceids
        serializer = RDRResource_Serializer_Plus(objects, context={'request': request}, many=True)
        if returnformat != 'html':
            return Response(serializer.data)
        else:
            return render(request, 'warehouse_views/warehouse_resources.html', {'resource_list': serializer.data})

class RDR_List_Active(APIView):
    '''
        ### RDR information about ACTIVE XSEDE resources, meaning:
            Provider level is: Level 1 or Level 2
            Status is: friendly, coming soon, pre-production, production, post-production
            
        Excludes: Non-XSEDE, Provider Level 3, Status Decomissioned
        
        Optional selection argument(s):
        ```
            info_siteid=<siteid>
        ```
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
            sort=<field>
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        returnformat = request.query_params.get('format', None)
        try:
            sort_by = request.GET.get('sort')
            objects = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='SUB', result='OBJECTS').order_by('info_resourceid').order_by(sort_by)
        except:
            objects = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='SUB', result='OBJECTS').order_by('info_resourceid')
        for o in objects:
            o.Active = True
        serializer = RDRResource_Serializer_Plus(objects, context={'request': request}, many=True)
        if returnformat != 'html':
            return Response(serializer.data)
        else:
            return render(request, 'warehouse_views/warehouse_resources.html', {'resource_list': serializer.data})

class Resource_List_XDCDB_Active(APIView):
    '''
        ### XDCDB resource information about ACTIVE XSEDE resources, meaning:
            Provider level is: Level 1 or Level 2
            Status is: friendly, coming soon, pre-production, production, post-production
            
        Excludes: Non-XSEDE, Provider Level 3, Status Decomissioned
        
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='ALL', result='RESOURCEID')
        try:
            sort_by = request.GET.get('sort')
            objects = TGResource.objects.filter(ResourceID__in=active_resourceids).order_by('ResourceID').order_by(sort_by)
        except:
            objects = objects = TGResource.objects.filter(ResourceID__in=active_resourceids).order_by('ResourceID')
        returnformat = request.query_params.get('format', None)
        objects = TGResource.objects.filter(ResourceID__in=active_resourceids).order_by('ResourceID')
        serializer = XSEDEResource_Serializer(objects, many=True)
        if returnformat != 'html':
            return Response(serializer.data)
        else:
            context = {'xdcdb_list': serializer.data}
            return render(request, 'warehouse_views/xdcdb_resources.html', context)

class Resource_List_CSA_Active(APIView):
    '''
        ### RDR Community Software Area (CSA) information about ACTIVE XSEDE resources, meaning:
            Provider level is: Level 1 or Level 2
            Status is: friendly, coming soon, pre-production, production, post-production
            Community Software Area Support is: True
            
        Excludes: Non-XSEDE, Provider Level 3, Status Decomissioned, no CSA Support
        
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None):
        csa_resources = RDR_Active_Resources(affiliation='XSEDE', allocated=False, type='SUB', result='OBJECTS')
        objects = []
        for res in csa_resources:
            if str(res.other_attributes.get('community_software_area', '')).lower() == 'true':
                objects.append(res)
        serializer = RDR_CSA_Serializer(objects, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='warehouse_views/csa_resources.html')

class RDR_Detail(APIView):
    '''
        ### RDR detailed information
        
        Required selection argument(s):
        ```
            resourceid=<info_resourceid>
        ```
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
#    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        returnformat = request.query_params.get('format', None)
        if 'resourceid' in self.kwargs:
            try:
                objects = RDRResource.objects.filter(info_resourceid__exact=uri_to_iri(self.kwargs['resourceid']),rdr_type__exact='resource')
            except RDRResource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if not objects:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if returnformat != 'html':
            serializer = Generic_Resource_Serializer(objects[0])
            return Response(serializer.data)
        else:
            serializer = Generic_Resource_Serializer(objects[0])
            context = {'resource_details': serializer.data}
            return render(request, 'warehouse_views/resource_details.html', context)

class Software_Full(APIView):
    '''
        ### Software detailed information
        
        Optional selection argument(s):
        ```
            AppName=<appname>
            resourceid=<info_resourceid>
            ID=<id>
        ```
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = ApplicationHandle.objects.get(pk=uri_to_iri(self.kwargs['id'])) # uri_to_iri translates %xx
            except ApplicationHandle.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = Software_Community_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            serializer = Software_Community_Serializer(objects, many=True)
#        elif 'siteid' in self.kwargs:
#            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['siteid'])
#            serializer = Software_Community_Serializer(objects, many=True)
        elif 'appname' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ApplicationEnvironment__AppName__exact=uri_to_iri(self.kwargs['appname']))
            serializer = Software_Community_Serializer(objects, many=True)
        else:
            objects = ApplicationHandle.objects.all()
            serializer = Software_Community_Serializer(objects, many=True)
        return Response(serializer.data)

class Software_XUP_v1_List(APIView):
    '''
        ### XUP Software Detail of XSEDE SP Supported Software
        
        Optional response argument(s):
        ```
            format={json,xml}                   (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='SUB', result='RESOURCEID')
        xsede_contact = 'https://info.xsede.org/wh1/xcsr-db/v1/supportcontacts/globalid/helpdesk.xsede.org/'
        objects = ApplicationHandle.objects.filter(ResourceID__in=active_resourceids).filter(ApplicationEnvironment__EntityJSON__Extension__SupportContact__exact=xsede_contact)
        serializer = Software_Full_Serializer(objects, many=True)
        return Response(serializer.data)

class Community_Software_XUP_v1_List(APIView):
    '''
        ### XUP Software Detail of Community Software Area (CSA) software
        
        Optional response argument(s):
        ```
            format={json,xml}                   (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        xsede_contact = 'https://info.xsede.org/wh1/xcsr-db/v1/supportcontacts/globalid/helpdesk.xsede.org/'
        objects = ApplicationHandle.objects.exclude(ApplicationEnvironment__EntityJSON__Extension__SupportContact__exact=xsede_contact)
        serializer = Software_Community_Serializer(objects, many=True)
        return Response(serializer.data)
