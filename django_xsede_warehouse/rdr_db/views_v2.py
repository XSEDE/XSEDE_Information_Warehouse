from django.db.models import Q
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rdr_db.models import *
from rdr_db.filters import *
from rdr_db.serializers import *
from itertools import chain
#import pdb

# Create your views here.
class RDRResource_XUP_v2_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,XMLRenderer,TemplateHTMLRenderer,)
    def get(self, request, format=None):
        returnformat = request.query_params.get('format', 'json')
        all_resources = RDR_Active_All_Resources()
        serializer = RDRResource_Serializer(all_resources, many=True)
        #return Response(serializer.data)
        if returnformat != 'html':
            return Response(serializer.data)
        else:
            return render(request, 'resources.html', {'resource_list': serializer.data})

class RDRResource_XUP_v3_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,XMLRenderer,TemplateHTMLRenderer,)
    def get(self, request, format=None):
        sub_objects = RDRResource.objects.filter(
                                              (Q(rdr_type='compute') | Q(rdr_type='storage')) &
                                              (Q(current_statuses__icontains='friendly') |
                                               Q(current_statuses__icontains='coming soon') |
                                               Q(current_statuses__icontains='pre-production') |
                                               Q(current_statuses__istartswith='production') |
                                               Q(current_statuses__icontains=',production') |
                                               Q(current_statuses__icontains='post-production')) &
                                              (Q(other_attributes__is_visualization='true') |
                                               Q(other_attributes__allocations_info__allocable_type='ComputeResource') |
                                               Q(other_attributes__allocations_info__allocable_type='StorageResource'))
                                              )

        sub_parent_ids = sub_objects.values_list('parent_resource', flat=True)
        
        base_resources = RDRResource.objects.filter(Q(other_attributes__project_affiliation='XSEDE') &
                                             Q(rdr_type='resource') &
                                             (Q(other_attributes__provider_level='XSEDE Level 1') |
                                              Q(other_attributes__provider_level='XSEDE Level 2')) &
                                             (Q(current_statuses__icontains='friendly') |
                                              Q(current_statuses__icontains='coming soon') |
                                              Q(current_statuses__icontains='pre-production') |
                                              Q(current_statuses__istartswith='production') |
                                              Q(current_statuses__icontains=',production') |
                                              Q(current_statuses__icontains='post-production')) &
                                             Q(rdr_resource_id__in=sub_parent_ids)
                                             )
        base_pks = base_resources.values_list('rdr_resource_id', flat=True)
        sub_objects = RDRResource.objects.filter(Q(parent_resource__in=base_pks) &
                                              Q(rdr_type='compute') &
                                              (Q(current_statuses__icontains='friendly') |
                                               Q(current_statuses__icontains='coming soon') |
                                               Q(current_statuses__icontains='pre-production') |
                                               Q(current_statuses__istartswith='production') |
                                               Q(current_statuses__icontains=',production') |
                                               Q(current_statuses__icontains='post-production')) &
                                              (Q(other_attributes__is_visualization='true') |
                                               Q(other_attributes__allocations_info__allocable_type='ComputeResource'))
                                              )
        objects = chain(base_resources, sub_objects)
        serializer = RDRResource_Serializer(objects, many=True)
        #return Response(serializer.data)
        if returnformat != 'html':
            return Response(serializer.data)
        else:
            return render(request, 'resourcesv3.html', {'resource_list': serializer.data})
