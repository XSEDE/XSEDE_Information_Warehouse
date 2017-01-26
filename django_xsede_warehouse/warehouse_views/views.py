from django.db.models import Q
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import uri_to_iri

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
#from rdr_db.models import RDRResource
from rdr_db.filters import *
from glue2_db.models import ApplicationHandle
from xdcdb.models import *
from xdcdb.serializers import *
from warehouse_views.serializers import Software_Full_Serializer
import pdb

#def Active_ResourceIDs():
#    base_resources = RDRResource.objects.filter(
#                                         Q(rdr_type='resource') &
#                                         Q(other_attributes__project_affiliation='XSEDE') &
#                                         Q(other_attributes__xsede_services_only=False) &
#                                         (Q(other_attributes__provider_level='XSEDE Level 1') |
#                                          Q(other_attributes__provider_level='XSEDE Level 2')) &
#                                         ~Q(info_resourceid='stand-alone.tg.teragrid.org') &
#                                         ~Q(info_resourceid='futuregrid0.futuregrid.xsede.org') &
#                                         ~Q(info_resourceid='Abe-QB-Grid.teragrid.org') &
#                                         (Q(current_statuses__icontains='friendly') |
#                                          Q(current_statuses__icontains='coming soon') |
#                                          Q(current_statuses__icontains='pre-production') |
#                                          Q(current_statuses__istartswith='production') |
#                                          Q(current_statuses__icontains=',production') |
#                                          Q(current_statuses__icontains='post-production'))
#                                         )
#    base_pks = base_resources.values_list('rdr_resource_id', flat=True)
#    sub_resources = RDRResource.objects.filter(
#                                         Q(parent_resource__in=base_pks) &
#                                         (Q(current_statuses__icontains='friendly') |
#                                          Q(current_statuses__icontains='coming soon') |
#                                          Q(current_statuses__icontains='pre-production') |
#                                          Q(current_statuses__istartswith='production') |
#                                          Q(current_statuses__icontains=',production') |
#                                          Q(current_statuses__icontains='post-production')) &
#                                         ( (Q(rdr_type='compute') & Q(other_attributes__is_visualization=True)) |
#                                           (Q(rdr_type='compute') & Q(other_attributes__allocations_info__allocable_type='ComputeResource')) |
#                                           (Q(rdr_type='storage'))
#                                         )
#                                         )
#    # list() forces evaluation so that we avoid issues with a sub-query in a different schema
#    return(list(sub_resources.values_list('info_resourceid', flat=True)))

# Create your views here.
class Resource_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='ALL', result='RESOURCEID')
        objects = RDRResource.objects.filter(rdr_type='resource').order_by('info_resourceid')
        for o in objects:
            o.Active = o.info_resourceid in active_resourceids
        c = Context({'resource_list': objects})
        return render(request, 'resources.html', c)

class Resource_List_Active(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='SUB', result='OBJECTS').order_by('info_resourceid')
        for o in objects:
            o.Active = True
        c = Context({'resource_list': objects})
        return render(request, 'resources.html', c)

class Resource_List_XDCDB_Active(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='ALL', result='RESOURCEID')
        ids = []
        for item in active_resourceids:
            ids.append(item[0])
        objects = TGResource.objects.filter(ResourceID__in=ids).order_by('ResourceID')
        c = Context({'xdcdb_list': objects})
        return render(request, 'xdcdb_resources.html', c)

class Software_Full(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None, **kwargs):
        if 'id' in self.kwargs:
            try:
                object = ApplicationHandle.objects.get(pk=uri_to_iri(self.kwargs['id'])) # uri_to_iri translates %xx
            except ApplicationHandle.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = Software_Full_Serializer(object)
        elif 'resourceid' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['resourceid'])
            serializer = Software_Full_Serializer(objects, many=True)
#        elif 'siteid' in self.kwargs:
#            objects = ApplicationHandle.objects.filter(ResourceID__exact=self.kwargs['siteid'])
#            serializer = Software_Full_Serializer(objects, many=True)
        elif 'appname' in self.kwargs:
            objects = ApplicationHandle.objects.filter(ApplicationEnvironment__AppName__exact=uri_to_iri(self.kwargs['appname']))
            serializer = Software_Full_Serializer(objects, many=True)
        else:
            objects = ApplicationHandle.objects.all()
            serializer = Software_Full_Serializer(objects, many=True)
        return Response(serializer.data)

class Software_XUP_v1_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
#        active_resourceids = Active_ResourceIDs()
        active_resourceids = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='SUB', result='RESOURCEID')
        objects = ApplicationHandle.objects.filter(ResourceID__in=active_resourceids)
        serializer = Software_Full_Serializer(objects, many=True)
        return Response(serializer.data)
