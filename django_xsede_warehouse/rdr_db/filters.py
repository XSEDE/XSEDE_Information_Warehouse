from django.db.models import Q
from rdr_db.models import RDRResource
from itertools import chain

###############################################################################
# XUP Active Resource Filtering Criteria
#
# With ACTIVE statuses being:
#   friendly | coming soon | pre-production | production | post-production
#
# An Active BASE RESOURCE is
#      rdr_type='resource'
#  and other_attributes.project_affiliation='XSEDE'
#  and xsede_services_only is False
#  and other_attributes.provider_level in ['XSEDE Level 1', 'XSEDE Level 2']
#  and current_statuses include ACTIVE
#
# An Active SUB-RESOURCE of the above BASE RESOURCES is ONE of:
#      rdr_type='compute'
#   and current_statuses include ACTIVE
#   and other_attributes.is_visualization is True
# OR
#      rdr_type='compute'
#   and current_statuses include ACTIVE
#   and other_attributes.allocations_info.allocable_type = 'ComputeResource'
# OR
#      rdr_type='storage'
#   and current_statuses include ACTIVE
###############################################################################

def RDR_Active_Sub_ResourceIDs():
    # Active base resources
    base_resources = RDRResource.objects.filter(
                                         Q(rdr_type='resource') &
                                         Q(other_attributes__project_affiliation='XSEDE') &
                                         Q(other_attributes__xsede_services_only=False) &
                                         (Q(other_attributes__provider_level='XSEDE Level 1') |
                                          Q(other_attributes__provider_level='XSEDE Level 2')) &
                                         ~Q(info_resourceid='stand-alone.tg.teragrid.org') &
                                         ~Q(info_resourceid='futuregrid0.futuregrid.xsede.org') &
                                         ~Q(info_resourceid='Abe-QB-Grid.teragrid.org') &
                                         (Q(current_statuses__icontains='friendly') |
                                          Q(current_statuses__icontains='coming soon') |
                                          Q(current_statuses__icontains='pre-production') |
                                          Q(current_statuses__istartswith='production') |
                                          Q(current_statuses__icontains=',production') |
                                          Q(current_statuses__icontains='post-production'))
                                         )
    base_pks = base_resources.values_list('rdr_resource_id', flat=True)
    # Active sub-resources of active base resources
    sub_resources = RDRResource.objects.filter(
                                         Q(parent_resource__in=base_pks) &
                                         (Q(current_statuses__icontains='friendly') |
                                          Q(current_statuses__icontains='coming soon') |
                                          Q(current_statuses__icontains='pre-production') |
                                          Q(current_statuses__istartswith='production') |
                                          Q(current_statuses__icontains=',production') |
                                          Q(current_statuses__icontains='post-production')) &
                                         ( (Q(rdr_type='compute') & Q(other_attributes__is_visualization=True)) |
                                           (Q(rdr_type='compute') & Q(other_attributes__allocations_info__allocable_type='ComputeResource')) |
                                           (Q(rdr_type='storage'))
                                         )
                                         )
    # list() forces evaluation so that we avoid issues with a sub-query in a different schema
    return(list(sub_resources.values_list('info_resourceid', flat=True)))

def RDR_Active_Sub_Resources():
    # Active base resources
    base_resources = RDRResource.objects.filter(
                                         Q(rdr_type='resource') &
                                         Q(other_attributes__project_affiliation='XSEDE') &
                                         Q(other_attributes__xsede_services_only=False) &
                                         (Q(other_attributes__provider_level='XSEDE Level 1') |
                                          Q(other_attributes__provider_level='XSEDE Level 2')) &
                                         ~Q(info_resourceid='stand-alone.tg.teragrid.org') &
                                         ~Q(info_resourceid='futuregrid0.futuregrid.xsede.org') &
                                         ~Q(info_resourceid='Abe-QB-Grid.teragrid.org') &
                                         (Q(current_statuses__icontains='friendly') |
                                          Q(current_statuses__icontains='coming soon') |
                                          Q(current_statuses__icontains='pre-production') |
                                          Q(current_statuses__istartswith='production') |
                                          Q(current_statuses__icontains=',production') |
                                          Q(current_statuses__icontains='post-production'))
                                         )
    base_pks = base_resources.values_list('rdr_resource_id', flat=True)
    # Active sub-resources of active base resources
    sub_resources = RDRResource.objects.filter(
                                         Q(parent_resource__in=base_pks) &
                                         (Q(current_statuses__icontains='friendly') |
                                          Q(current_statuses__icontains='coming soon') |
                                          Q(current_statuses__icontains='pre-production') |
                                          Q(current_statuses__istartswith='production') |
                                          Q(current_statuses__icontains=',production') |
                                          Q(current_statuses__icontains='post-production')) &
                                         ( (Q(rdr_type='compute') & Q(other_attributes__is_visualization=True)) |
                                           (Q(rdr_type='compute') & Q(other_attributes__allocations_info__allocable_type='ComputeResource')) |
                                           (Q(rdr_type='storage'))
                                         )
                                         )
    return(sub_resources)

def RDR_Active_All_ResourceIDs():
    base_resources = RDRResource.objects.filter(
                                         Q(rdr_type='resource') &
                                         Q(other_attributes__project_affiliation='XSEDE') &
                                         Q(other_attributes__xsede_services_only=False) &
                                         (Q(other_attributes__provider_level='XSEDE Level 1') |
                                          Q(other_attributes__provider_level='XSEDE Level 2')) &
                                         ~Q(info_resourceid='stand-alone.tg.teragrid.org') &
                                         ~Q(info_resourceid='futuregrid0.futuregrid.xsede.org') &
                                         ~Q(info_resourceid='Abe-QB-Grid.teragrid.org') &
                                         (Q(current_statuses__icontains='friendly') |
                                          Q(current_statuses__icontains='coming soon') |
                                          Q(current_statuses__icontains='pre-production') |
                                          Q(current_statuses__istartswith='production') |
                                          Q(current_statuses__icontains=',production') |
                                          Q(current_statuses__icontains='post-production'))
                                         )
    base_pks = base_resources.values_list('rdr_resource_id', flat=True)
    sub_resources = RDRResource.objects.filter(
                                         Q(parent_resource__in=base_pks) &
                                         (Q(current_statuses__icontains='friendly') |
                                          Q(current_statuses__icontains='coming soon') |
                                          Q(current_statuses__icontains='pre-production') |
                                          Q(current_statuses__istartswith='production') |
                                          Q(current_statuses__icontains=',production') |
                                          Q(current_statuses__icontains='post-production')) &
                                         ( (Q(rdr_type='compute') & Q(other_attributes__is_visualization=True)) |
                                           (Q(rdr_type='compute') & Q(other_attributes__allocations_info__allocable_type='ComputeResource')) |
                                           (Q(rdr_type='storage'))
                                         )
                                         )
#    all_resources = chain(base_resources, sub_resources)
    # list() forces evaluation so that we avoid issues with a sub-query in a different schema
    return(list(chain(base_resources.values_list('info_resourceid'), sub_resources.values_list('info_resourceid'))))
#    return(list(all_resources.values_list('info_resourceid', flat=True)))

def RDR_Active_All_Resources():
    base_resources = RDRResource.objects.filter(
                                         Q(rdr_type='resource') &
                                         Q(other_attributes__project_affiliation='XSEDE') &
                                         Q(other_attributes__xsede_services_only=False) &
                                         (Q(other_attributes__provider_level='XSEDE Level 1') |
                                          Q(other_attributes__provider_level='XSEDE Level 2')) &
                                         ~Q(info_resourceid='stand-alone.tg.teragrid.org') &
                                         ~Q(info_resourceid='futuregrid0.futuregrid.xsede.org') &
                                         ~Q(info_resourceid='Abe-QB-Grid.teragrid.org') &
                                         (Q(current_statuses__icontains='friendly') |
                                          Q(current_statuses__icontains='coming soon') |
                                          Q(current_statuses__icontains='pre-production') |
                                          Q(current_statuses__istartswith='production') |
                                          Q(current_statuses__icontains=',production') |
                                          Q(current_statuses__icontains='post-production'))
                                         )
    base_pks = base_resources.values_list('rdr_resource_id', flat=True)
    sub_resources = RDRResource.objects.filter(
                                         Q(parent_resource__in=base_pks) &
                                         (Q(current_statuses__icontains='friendly') |
                                          Q(current_statuses__icontains='coming soon') |
                                          Q(current_statuses__icontains='pre-production') |
                                          Q(current_statuses__istartswith='production') |
                                          Q(current_statuses__icontains=',production') |
                                          Q(current_statuses__icontains='post-production')) &
                                         ( (Q(rdr_type='compute') & Q(other_attributes__is_visualization=True)) |
                                           (Q(rdr_type='compute') & Q(other_attributes__allocations_info__allocable_type='ComputeResource')) |
                                           (Q(rdr_type='storage'))
                                         )
                                         )
    return(chain(base_resources, sub_resources))