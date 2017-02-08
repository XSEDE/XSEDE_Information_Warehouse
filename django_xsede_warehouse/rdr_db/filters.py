from django.db.models import Q
from rdr_db.models import RDRResource
from itertools import chain

###############################################################################
# Active RDR Resource Filtering Criteria
#
# Arguments:
#   affiliation: XSEDE federated, otherwise ALL
#   allocated: True=allocated Level 1 and 2, otherwise ALL
#   type: SUB=sub-resources only, otherwise ALL (parent and sub)
#   result: return RESOURCEID, otherwise model objects by default
#
# With the ACTIVE status set being:
#   friendly | coming soon | pre-production | production | post-production
#
# An Active BASE RESOURCE is
#      rdr_type='resource'
#  and xsede_services_only is False (True means this isn't a user facing service)
#  and provider_level in ['XSEDE Level 1', 'XSEDE Level 2']
#  and current_statuses in ACTIVE status set
#
# An Active SUB-RESOURCE of the above BASE RESOURCES is ONE of:
#      rdr_type='compute'
#   and current_statuses in ACTIVE status set
#   and other_attributes.is_visualization is True
# OR
#      rdr_type='compute'
#   and current_statuses in ACTIVE status set
#   and other_attributes.allocations_info.allocable_type = 'ComputeResource'
# OR
#      rdr_type='storage'
#   and current_statuses in ACTIVE status set
#
# NOTES:
#   list() forces evaluation so that we avoid issues with a sub-query in a different schema

###############################################################################

# Not Active_Sub or Active_All

def RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='SUB', result='OBJECTS'):
    # Active base resources
    if allocated:
        parent_resources = RDRResource.objects.filter(
                                                Q(rdr_type='resource') &
                                                Q(project_affiliation=affiliation) &
                                                Q(other_attributes__xsede_services_only=False) &
                                                (Q(provider_level='XSEDE Level 1') |
                                                 Q(provider_level='XSEDE Level 2')) &
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
    else:
        parent_resources = RDRResource.objects.filter(
                                                Q(rdr_type='resource') &
                                                Q(project_affiliation=affiliation) &
                                                Q(other_attributes__xsede_services_only=False) &
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
    parent_ids = parent_resources.values_list('rdr_resource_id', flat=True)
    # Active sub-resources of active parent resources
    if allocated:
        child_resource = RDRResource.objects.filter(
                                               Q(parent_resource__in=parent_ids) &
                                               (Q(current_statuses__icontains='friendly') |
                                                Q(current_statuses__icontains='coming soon') |
                                                Q(current_statuses__icontains='pre-production') |
                                                Q(current_statuses__istartswith='production') |
                                                Q(current_statuses__icontains=',production') |
                                                Q(current_statuses__icontains='post-production')) &
                                               ((Q(rdr_type='compute') & Q(other_attributes__is_visualization=True)) |
                                                (Q(rdr_type='compute') & Q(other_attributes__allocations_info__allocable_type='ComputeResource')) |
                                                (Q(rdr_type='storage'))
                                                )
                                                   )
    else:
        child_resource = RDRResource.objects.filter(
                                               Q(parent_resource__in=parent_ids) &
                                               (Q(current_statuses__icontains='friendly') |
                                                Q(current_statuses__icontains='coming soon') |
                                                Q(current_statuses__icontains='pre-production') |
                                                Q(current_statuses__istartswith='production') |
                                                Q(current_statuses__icontains=',production') |
                                                Q(current_statuses__icontains='post-production')) &
                                               (Q(rdr_type='compute') | Q(rdr_type='storage'))
                                                   )
    if result.upper() == 'RESOURCEID':
        if type.upper() == 'SUB':
            return(list(child_resource.values_list('info_resourceid', flat=True)))
        else:
            return(list(chain(parent_resources.values_list('info_resourceid', flat=True), \
                              child_resource.values_list('info_resourceid', flat=True))))
    else: # Model objects
        if type.upper() == 'SUB':
            return(child_resource)
        else:
            return(chain(parent_resources, child_resource))
