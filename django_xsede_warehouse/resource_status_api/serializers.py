from django.core.urlresolvers import reverse, get_script_prefix
from django.utils.encoding import uri_to_iri
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rdr_db.models import RDRResource
from monitoring_db.models import TestResult
from outages.models import Outages
import pdb

class Resource_Status_Serializer(serializers.Serializer):
    # Resource identifiers and descriptions
    # pdb.set_trace()
    ResourceID = serializers.CharField(source='info_resourceid')
    SiteID = serializers.CharField(source='info_siteid')
    DisplayName = serializers.CharField(source='resource_descriptive_name')

    RDR_Label = ''
    RDR_Declared_Status = serializers.SerializerMethodField()

    Outage_Label = ''
    Outage_Status = serializers.SerializerMethodField()

    Monitor_Label = ''
    Monitoring_Status = serializers.SerializerMethodField()

    Overall_Status = serializers.SerializerMethodField()

    def get_RDR_Declared_Status(self, RDRResource):
# First of: decommissioned, retired, post-production, production, \
#           pre-production, friendly, coming soon, or <blank>
        status_list = RDRResource.current_statuses.split(',')
        RDR_Summary = ''
        for ordered_status in ['decommissioned', 'retired', 'post-production', 'production', 'pre-production', 'friendly', 'coming_soon']:
            if ordered_status in status_list:
                if ordered_status == 'production':
                    self.RDR_Label = 'Green'
                elif ordered_status in ['post-production', 'pre-production']:
                    self.RDR_Label = 'Yellow'
                else:
                    self.RDR_Label = 'Red'
                RDR_Summary = 'In %s' % ordered_status

        http_request = self.context.get("request")
        if http_request:
            RDR_URL = http_request.build_absolute_uri(uri_to_iri(reverse('rdr-xup-detail', args=[RDRResource.rdr_resource_id])))
        else:
            RDR_URL = ''

        return {'Label': self.RDR_Label,
                'Summary': RDR_Summary,
                'References_URLs': RDR_URL}

    def get_Outage_Status(self, RDRResource):
        now = timezone.now()
        outsearch = Outages.objects.filter(ResourceID=RDRResource.info_resourceid, OutageStart__lte=now, OutageEnd__gte=now)
        outurls = set()
        http_request = self.context.get("request")
        for out in outsearch:
            if http_request:
                outurls.add(http_request.build_absolute_uri(uri_to_iri(reverse('outages-detail', args=[out.OutageID]))))
        if outsearch:
            self.Outage_Label = 'Red'
            Outage_Summary = '%s current outage(s)' % len(outsearch)
        else:
            self.Outage_Label = 'Green'
            Outage_Summary = ''

        return {'Label': self.Outage_Label,
                'Summary': Outage_Summary,
                'References_URLs': outurls}

    def get_Monitoring_Status(self, RDRResource):
        monsearch = TestResult.objects.filter(ResourceID=RDRResource.info_resourceid)
        monfail = set()
        monurls = set()
        http_request = self.context.get("request")
        for mon in monsearch:
            if mon.Result == 'Pass':
                continue
            monfail.add(mon.ID)
            if http_request:
                monurls.add(http_request.build_absolute_uri(uri_to_iri(reverse('testresult-detail', args=[mon.ID]))))
        if not monfail:
            self.Monitor_Label = 'Green'
            Monitor_Summary = ''
        elif len(monfail) < len(monsearch):
            self.Monitor_Label = 'Yellow'
            Monitor_Summary = 'Some tests failing (%s of %s)' % (len(monfail), len(monsearch))
        else:
            self.Monitor_Label = 'Red'
            Monitor_Summary = 'All %s tests failing' % len(monfail)
                
        return {'Label': self.Monitor_Label,
                'Summary': Monitor_Summary,
                'Reference_URLs': monurls}

#    def get_monitor_fields(self, RDRResource):
#        return dict([('monitor_resource_id', RDRResource.rdr_resource_id), ])

    def get_Overall_Status(self, RDRResource):
    #   Overall status fields
    #   Green: rdr = (pre-production, production, post-production) and NO outages and NO test failures
    #   Yellow: some tests pass
    #   Red: no tests pass
        if self.RDR_Label in ['Green', 'Yellow'] and \
                self.Outage_Label == 'Green' and \
                self.Monitor_Label == 'Green':
            Overall_Label = 'Green'
            Overall_Summary = 'No issues'
        elif self.Monitor_Label in ['Green', 'Yellow']:
            Overall_Label = 'Yellow'
            Overall_Summary = 'A partial outage detected'
        else:
            Overall_Label = 'Red'
            Overall_Summary = 'System not functional'
        now = timezone.now()
        
        return {'Label': Overall_Label,
                'Summary': Overall_Summary,
                'Status_at': now}

    class Meta:
        model = RDRResource
        fields = ('rdr_resource_id', 'rdr_type', 'info_resourceid', 'info_siteid',
                  'resource_descriptive_name', 'resource_status', 'current_statuses')
