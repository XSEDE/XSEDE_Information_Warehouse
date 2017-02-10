from django.core.urlresolvers import reverse, get_script_prefix
from django.utils.encoding import uri_to_iri
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rdr_db.models import RDRResource
from monitoring_db.models import TestResult
from outages.models import Outages
from processing_status.models import ProcessingRecord
import datetime
import pdb

class Resource_Status_Serializer(serializers.Serializer):
    # Resource identifiers and descriptions
    ResourceID = serializers.CharField(source='info_resourceid')
    SiteID = serializers.CharField(source='info_siteid')
    DisplayName = serializers.CharField(source='resource_descriptive_name')
    ProjectAffiliation = serializers.CharField(source='project_affiliation')
    ProviderLevel = serializers.CharField(source='provider_level')

    RDR_Label = ''
    RDR_Summary = ''
    RDR_Declared_Status = serializers.SerializerMethodField()

    Outage_Label = ''
    Outage_Summary = ''
    Outage_Status = serializers.SerializerMethodField()

    Monitor_Label = ''
    Monitor_Summary = ''
    Monitoring_Status = serializers.SerializerMethodField()

    Overall_Status = serializers.SerializerMethodField()

    def get_RDR_Declared_Status(self, RDRResource):
        if RDRResource.latest_status in ['production']:
            self.RDR_Label = 'Green'
        elif RDRResource.latest_status in ['post-production', 'pre-production']:
            self.RDR_Label = 'Yellow'
        else:
            self.RDR_Label = 'Red'
        self.RDR_Summary = 'In "{}"'.format(RDRResource.latest_status)
        if RDRResource.latest_status_begin:
            self.RDR_Summary += ' starting {}'.format(RDRResource.latest_status_begin)
        if RDRResource.latest_status_end:
            self.RDR_Summary += ' until {}'.format(RDRResource.latest_status_end)

        http_request = self.context.get("request")
        if http_request:
            RDR_URL = http_request.build_absolute_uri(uri_to_iri(reverse('rdr-xup-detail', args=[RDRResource.rdr_resource_id])))
        else:
            RDR_URL = ''

        return {'Label': self.RDR_Label,
                'Declared_Status': RDRResource.latest_status,
                'Declared_Status_Begin': RDRResource.latest_status_begin,
                'Declared_Status_End': RDRResource.latest_status_end,
                'Summary': self.RDR_Summary,
                'References_URLs': RDR_URL}

    def get_Outage_Status(self, RDRResource):
        now = timezone.now()
        outsearch = Outages.objects.filter(ResourceID=RDRResource.info_resourceid, OutageStart__lte=now, OutageEnd__gte=now)
        outurls = set()
        Full_Outage = False
        http_request = self.context.get("request")
        for out in outsearch:
            if http_request:
                outurls.add(http_request.build_absolute_uri(uri_to_iri(reverse('outages-detail', args=[out.OutageID]))))
            if out.OutageType.upper() == 'FULL':
                Full_Outage = True
        if Full_Outage:
            self.Outage_Label = 'Red'
            self.Outage_Summary = 'Full outage reported'
        elif outsearch:
            self.Outage_Label = 'Yellow'
            self.Outage_Summary = 'Partial outage repoted (%s)' % len(outsearch)
        else:
            self.Outage_Label = 'Green'
            self.Outage_Summary = ''

        return {'Label': self.Outage_Label,
                'Summary': self.Outage_Summary,
                'References_URLs': outurls}

    def get_Monitoring_Status(self, RDRResource):
        monsearch = TestResult.objects.filter(ResourceID=RDRResource.info_resourceid)
        monfail = set()
        monurls = set()
        http_request = self.context.get("request")
        for mon in monsearch:
            if mon.Result.upper() in ['PASS', 'SUCCESS']:
                continue
            monfail.add(mon.ID)
            if http_request:
                monurls.add(http_request.build_absolute_uri(uri_to_iri(reverse('testresult-detail', args=[mon.ID]))))
        if not monfail:
            self.Monitor_Label = 'Green'
        elif len(monfail) < len(monsearch):
            self.Monitor_Label = 'Yellow'
            self.Monitor_Summary = '%s of %s tests failing' % (len(monfail), len(monsearch))
        else:
            self.Monitor_Label = 'Red'
            self.Monitor_Summary = 'All %s tests failing' % len(monfail)
                
        return {'Label': self.Monitor_Label,
                'Summary': self.Monitor_Summary,
                'Reference_URLs': monurls}

    def get_Overall_Status(self, RDRResource):
    #   Overall Status algorithm
    #   Red: RDR declared status is not Green(production) or Yellow(pre-production, post-production)
    #         or Red(FULL) outage declared
    #         or Red(ALL) tests are failing
    #   Yellow: Yellow(PARTIAL) outage declared
    #         or Yellow(SOME) tests are failing
    #   Green: Green everything
    #         allowing RDR declared Yellow(pre-production, post-production)
        Summary_Items = []
        Summary_Severity = 0
        if self.RDR_Label not in ['Green', 'Yellow']:
            Summary_Items.append(self.RDR_Summary)
            Summary_Severity = max(2, Summary_Severity)
        if self.Outage_Label == 'Red':
            Summary_Items.append(self.Outage_Summary)
            Summary_Severity = max(2, Summary_Severity)
        if self.Monitor_Label == 'Red':
            Summary_Items.append(self.Monitor_Summary)
            Summary_Severity = max(2, Summary_Severity)
        if Summary_Severity == 0:
            # RDR_Label in ['Green', 'Yellow'] and Outage_Label != 'Red' and Monitor_Label != 'Red'
            if self.Outage_Label == 'Yellow':
                Summary_Items.append(self.Outage_Summary)
                Summary_Severity = max(1, Summary_Severity)
            if self.Monitor_Label == 'Yellow':
                Summary_Items.append(self.Monitor_Summary)
                Summary_Severity = max(1, Summary_Severity)
            if Summary_Severity == 0:
                Summary_Items.append('System operating normally')
        
        return {'Label': ['Green', 'Yellow', 'Red'][Summary_Severity],
                'Summary': '; '.join(Summary_Items),
                'Status_at': timezone.now()}

    class Meta:
        model = RDRResource
        fields = ('rdr_resource_id', 'rdr_type', 'info_resourceid', 'info_siteid',
                  'resource_descriptive_name', 'resource_status', 'current_statuses',
                  'latest_status', 'latest_status_begin', 'latest_status_end',
                  'project_affiliation', 'provider_level')

class Resource_Ops_Status_Serializer(serializers.Serializer):
    # Resource identifiers and descriptions
    ResourceID = serializers.CharField(source='info_resourceid')
    SiteID = serializers.CharField(source='info_siteid')
    DisplayName = serializers.CharField(source='resource_descriptive_name')
    ProjectAffiliation = serializers.CharField(source='project_affiliation')
    ProviderLevel = serializers.CharField(source='provider_level')
   
    RDR_Label = ''
    RDR_Summary = ''
    RDR_Declared_Status = serializers.SerializerMethodField()

    Outage_Label = ''
    Outage_Summary = ''
    Outage_Status = serializers.SerializerMethodField()

    Monitor_Label = ''
    Monitor_Summary = ''
    Monitoring_Status = serializers.SerializerMethodField()

    Publishing_Label = ''
    Publishing_Summary = ''
    Publishing_Status = serializers.SerializerMethodField()

    Overall_Status = serializers.SerializerMethodField()

    def get_RDR_Declared_Status(self, RDRResource):
        if RDRResource.latest_status in ['production']:
            self.RDR_Label = 'Green'
        elif RDRResource.latest_status in ['post-production', 'pre-production']:
            self.RDR_Label = 'Yellow'
        else:
            self.RDR_Label = 'Red'
        self.RDR_Summary = 'In "{}"'.format(RDRResource.latest_status)
        if RDRResource.latest_status_begin:
            self.RDR_Summary += ' starting {}'.format(RDRResource.latest_status_begin)
        if RDRResource.latest_status_end:
            self.RDR_Summary += ' until {}'.format(RDRResource.latest_status_end)

        http_request = self.context.get("request")
        if http_request:
            RDR_URL = http_request.build_absolute_uri(uri_to_iri(reverse('rdr-xup-detail', args=[RDRResource.rdr_resource_id])))
        else:
            RDR_URL = ''

        return {'Label': self.RDR_Label,
                'Declared_Status': RDRResource.latest_status,
                'Declared_Status_Begin': RDRResource.latest_status_begin,
                'Declared_Status_End': RDRResource.latest_status_end,
                'Summary': self.RDR_Summary,
                'References_URLs': RDR_URL}

    def get_Outage_Status(self, RDRResource):
        now = timezone.now()
        outsearch = Outages.objects.filter(ResourceID=RDRResource.info_resourceid, OutageStart__lte=now, OutageEnd__gte=now)
        outurls = set()
        Full_Outage = False
        http_request = self.context.get("request")
        for out in outsearch:
            if http_request:
                outurls.add(http_request.build_absolute_uri(uri_to_iri(reverse('outages-detail', args=[out.OutageID]))))
            if out.OutageType.upper() == 'FULL':
                Full_Outage = True
        if Full_Outage:
            self.Outage_Label = 'Red'
            self.Outage_Summary = 'Full outage reported'
        elif outsearch:
            self.Outage_Label = 'Yellow'
            self.Outage_Summary = 'Partial outage repoted (%s)' % len(outsearch)
        else:
            self.Outage_Label = 'Green'
            self.Outage_Summary = ''

        return {'Label': self.Outage_Label,
                'Summary': self.Outage_Summary,
                'References_URLs': outurls}

    def get_Monitoring_Status(self, RDRResource):
        monsearch = TestResult.objects.filter(ResourceID=RDRResource.info_resourceid)
        monfail = set()
        monurls = set()
        http_request = self.context.get("request")
        for mon in monsearch:
            if mon.Result.upper() in ['PASS', 'SUCCESS']:
                continue
            monfail.add(mon.ID)
            if http_request:
                monurls.add(http_request.build_absolute_uri(uri_to_iri(reverse('testresult-detail', args=[mon.ID]))))
        if not monfail:
            self.Monitor_Label = 'Green'
            Monitor_Summary = ''
        elif len(monfail) < len(monsearch):
            self.Monitor_Label = 'Yellow'
            self.Monitor_Summary = '%s of %s tests failing' % (len(monfail), len(monsearch))
        else:
            self.Monitor_Label = 'Red'
            self.Monitor_Summary = 'All %s tests failing' % len(monfail)
                
        return {'Label': self.Monitor_Label,
                'Summary': self.Monitor_Summary,
                'Reference_URLs': monurls}

    def get_Publishing_Status(self, RDRResource):
        pubsearch = ProcessingRecord.objects.filter(About=RDRResource.info_resourceid)
        puberror = set()
        pubwarning = set()
        puburls = set()
        http_request = self.context.get("request")
        for pub in pubsearch:
            add_url = False
            if pub.ProcessingEnd:
                delta = timezone.now() - pub.ProcessingEnd
            else:
                delta = timezone.now() - pub.ProcessingStart
            if pub.Topic == 'glue2.applications':
                if delta > datetime.timedelta(days=3):
                    puberror.add(pub)
                    add_url = True
                elif delta > datetime.timedelta(days=1):
                    pubwarning.add(pub)
                    add_url = True
            elif pub.Topic == 'glue2.compute':
                if delta > datetime.timedelta(hours=3):
                    puberror.add(pub)
                    add_url = True
                elif delta > datetime.timedelta(hours=1):
                    pubwarning.add(pub)
                    add_url = True
            if pub.ProcessingCode != '0':
                puberror.add(pub)
                add_url = True
            if http_request and add_url:
                puburls.add(http_request.build_absolute_uri(uri_to_iri(reverse('processingrecord-detail', args=[pub.ID]))))

        if not puberror and not pubwarning:
            self.Publishing_Label = 'Green'
        elif puberror:
            self.Publishing_Label = 'Red'
            self.Publishing_Summary = 'Some published information is old or missing ({} of {})'.format(len(puberror), len(pubsearch))
        else:
            self.Publishing_Label = 'Yellow'
            self.Publishing_Summary = 'Some published informaton is stale ({} of {})'.format(len(pubwarning), len(pubsearch))
        return {'Label': self.Publishing_Label,
            'Summary': self.Publishing_Summary,
            'Reference_URLs': puburls}

    def get_Overall_Status(self, RDRResource):
    #   Overall Status algorithm
    #   Red: RDR declared status is not Green(production) or Yellow(pre-production, post-production)
    #         or Red(FULL) outage declared
    #         or Red(ALL) tests are failing
    #         or Red(ANY) published information is old or missing)
    #   Yellow: Yellow(PARTIAL) outage declared
    #         or Yellow(SOME) tests are failing
    #   Green: Green everything
    #         allowing RDR Yellow(pre-production, post-production)
    #         allowing Publishing Yellow(stale information)
        Summary_Items = []
        Summary_Severity = 0
        if self.RDR_Label not in ['Green', 'Yellow']:
            Summary_Items.append(self.RDR_Summary)
            Summary_Severity = max(2, Summary_Severity)
        if self.Outage_Label == 'Red':
            Summary_Items.append(self.Outage_Summary)
            Summary_Severity = max(2, Summary_Severity)
        if self.Monitor_Label == 'Red':
            Summary_Items.append(self.Monitor_Summary)
            Summary_Severity = max(2, Summary_Severity)
        if self.Publishing_Label == 'Red':
            Summary_Items.append(self.Publishing_Summary)
            Summary_Severity = max(2, Summary_Severity)
        if Summary_Severity == 0:
            # RDR_Label in ['Green', 'Yellow'] and Outage_Label != 'Red' and Monitor_Label != 'Red' and Publishing_Label != 'Red'
            if self.Outage_Label == 'Yellow':
                Summary_Items.append(self.Outage_Summary)
                Summary_Severity = max(1, Summary_Severity)
            if self.Monitor_Label == 'Yellow':
                Summary_Items.append(self.Monitor_Summary)
                Summary_Severity = max(1, Summary_Severity)
            if self.Publishing_Label == 'Yellow':
                # Inform of Stale publishing without impacting the severity
                Summary_Items.append(self.Publishing_Summary)
#                Summary_Severity = max(1, Summary_Severity)
            elif Summary_Severity == 0:
                Summary_Items.append('System operating normally')
        
        return {'Label': ['Green', 'Yellow', 'Red'][Summary_Severity],
                'Summary': '; '.join(Summary_Items),
                'Status_at': timezone.now()}

    #   Overall Status algorithm (Operations Overall Status factors Publishing)
    #   Green: rdr declared status is one of (pre-production, production, post-production)
    #           and NO outages, NO test failures, NO publishing issues
    #   Red: rdr declared status is not one of (pre-production, production, post-production)
    #           or FULL outage declared, or ALL tests failing
    #   Yellow: otherwise
#        if self.RDR_Label in ['Green', 'Yellow'] and \
#                self.Outage_Label == 'Green' and \
#                self.Monitor_Label == 'Green' and \
#                self.Publishing_Label == 'Green':
#            Overall_Label = 'Green'
#            Overall_Summary = 'System operating normally'
#        elif self.RDR_Label not in ['Green', 'Yellow'] or \
#                self.Outage_Label == 'Red' or \
#                self.Monitor_Label == 'Red':
#            Overall_Label = 'Red'
#            Overall_Summary = 'System not production, has full outage, or is failing all testing'
#        else:
#            Overall_Label = 'Yellow'
#            Overall_Summary = 'System degraded'
#        
#        return {'Label': Overall_Label,
#                'Summary': Overall_Summary,
#                'Status_at': timezone.now()}

    #   Overall Status algorithm
    #   Green: rdr declared status is one of (pre-production, production, post-production)
    #           and NO outages, NO test failures, NO publishing issues
    #   Yellow: some tests pass
    #   Red: no tests pass
#        if self.RDR_Label in ['Green', 'Yellow'] and \
#                self.Outage_Label == 'Green' and \
#                self.Monitor_Label == 'Green' and \
#                self.Publishing_Label == 'Green':
#            Overall_Label = 'Green'
#            Overall_Summary = 'No issues'
#        elif self.RDR_Label not in ['Green', 'Yellow'] or \
#                self.Outage_Label == 'Red' or \
#                self.Monitor_Label == 'Red':
#            Overall_Label = 'Red'
#            Overall_Summary = 'System not production, has an outage, or is failing all monitoring'
#        else:
#            Overall_Label = 'Yellow'
#            Overall_Summary = 'System in degraded state'
#        now = timezone.now()
#        
#        return {'Label': Overall_Label,
#                'Summary': Overall_Summary,
#                'Status_at': now}

    class Meta:
        model = RDRResource
        fields = ('rdr_resource_id', 'rdr_type', 'info_resourceid', 'info_siteid',
                  'resource_descriptive_name', 'resource_status', 'current_statuses',
                  'latest_status', 'latest_status_begin', 'latest_status_end',
                  'project_affiliation', 'provider_level')
