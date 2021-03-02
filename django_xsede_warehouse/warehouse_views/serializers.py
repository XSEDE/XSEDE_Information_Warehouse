from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from glue2_db.models import ApplicationEnvironment, ApplicationHandle, Endpoint, ComputingManager, ExecutionEnvironment
from glue2_db.serializers import ApplicationHandle_DbSerializer
from outages.models import Outages
from rdr_db.models import RDRResource
from xdcdb.models import TGResource

#class JSONSerializerField(serializers.Field):
#    """ Serializer for JSONField -- required to make field writable"""
#    def to_internal_value(self, data):
#        return data
#    def to_representation(self, value):
#        return value


class Generic_Resource_Serializer(serializers.ModelSerializer):
    # Note: recommended_use and access_description come from compute sub-resources
    ResourceID = serializers.CharField(source='info_resourceid')
    SiteID = serializers.CharField(source='info_siteid')
    OrganizationAbbrev = serializers.SerializerMethodField()
    OrganizationName = serializers.SerializerMethodField()
    AmieName = serializers.SerializerMethodField()
    PopsName = serializers.SerializerMethodField()
    XcdbName = serializers.SerializerMethodField()
    class Meta:
        model = RDRResource
        fields = ('ResourceID', 'SiteID',
                  'rdr_resource_id', 'rdr_type', 'parent_resource',
                  'resource_descriptive_name', 'resource_description',
                  'current_statuses', 'latest_status', 'latest_status_begin', 'latest_status_end',
                  'recommended_use', 'access_description',
                  'project_affiliation', 'provider_level', 'updated_at',
                  'OrganizationAbbrev', 'OrganizationName',
                  'AmieName','PopsName', 'XcdbName')

    def get_OrganizationAbbrev(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.OrganizationAbbrev
        except TGResource.DoesNotExist:
            pass
        return None
    def get_OrganizationName(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.OrganizationName
        except TGResource.DoesNotExist:
            pass
        return None
    def get_AmieName(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.AmieName
        except TGResource.DoesNotExist:
            pass
        return None
    def get_PopsName(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.PopsName
        except TGResource.DoesNotExist:
            pass
        return None
    def get_XcdbName(self, RDRResource):
        try:
            XCDB_object = TGResource.objects.get(pk=RDRResource.info_resourceid)
            if XCDB_object:
                return XCDB_object.TgcdbResourceName
        except TGResource.DoesNotExist:
            pass
        return None

class Software_Full_Serializer(serializers.ModelSerializer):
    SiteID = serializers.SerializerMethodField('get_siteid')
    AppName = serializers.CharField(source='ApplicationEnvironment.AppName')
    AppVersion = serializers.CharField(source='ApplicationEnvironment.AppVersion')
    Description = serializers.CharField(source='ApplicationEnvironment.Description')
    Handle = serializers.SerializerMethodField('get_handle')
    Domain = serializers.SerializerMethodField('get_category')
    Keywords = serializers.SerializerMethodField('get_keywords')
    SupportStatus = serializers.SerializerMethodField('get_supportstatus')
    Repository = serializers.SerializerMethodField('get_repository')
    class Meta:
        model = ApplicationHandle
        fields = ('ResourceID', 'SiteID', 'AppName', 'AppVersion', 'Description', 'Handle', 'Domain',
                  'Keywords', 'SupportStatus', 'Repository', 'CreationTime','ID')

    def get_siteid(self, ApplicationHandle):
        try:
            RDR_object = RDRResource.objects.filter(rdr_type='resource').filter(info_resourceid=ApplicationHandle.ResourceID)
            if RDR_object and RDR_object[0] and RDR_object[0].info_siteid:
                return RDR_object[0].info_siteid
        except RDRResource.DoesNotExist:
            pass
        return None

    def get_handle(self, ApplicationHandle):
        return({'HandleType': ApplicationHandle.Type,
                'HandleKey': ApplicationHandle.Value
               })
    
    def get_category(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension']['Category']
        except:
            return []

    def get_keywords(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Keywords']
        except:
            return []

    def get_supportstatus(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension']['SupportStatus']
        except:
            return []

    def get_repository(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Repository']
        except:
            return []
            
# Same as Software_Full_Serializer but adds SupportContact
class Software_Community_Serializer(serializers.ModelSerializer):
    SiteID = serializers.SerializerMethodField('get_siteid')
    AppName = serializers.CharField(source='ApplicationEnvironment.AppName')
    AppVersion = serializers.CharField(source='ApplicationEnvironment.AppVersion')
    Description = serializers.CharField(source='ApplicationEnvironment.Description')
    Handle = serializers.SerializerMethodField('get_handle')
    Domain = serializers.SerializerMethodField('get_category')
    Keywords = serializers.SerializerMethodField('get_keywords')
    SupportStatus = serializers.SerializerMethodField('get_supportstatus')
    SupportContact = serializers.SerializerMethodField('get_supportcontact')
    Repository = serializers.SerializerMethodField('get_repository')
    class Meta:
        model = ApplicationHandle
        fields = ('ResourceID', 'SiteID', 'AppName', 'AppVersion', 'Description', 'Handle', 'Domain',
                  'Keywords', 'SupportStatus', 'SupportContact', 'Repository', 'CreationTime', 'ID')

    def get_siteid(self, ApplicationHandle):
        try:
            RDR_object = RDRResource.objects.filter(rdr_type='resource').filter(info_resourceid=ApplicationHandle.ResourceID)
            if RDR_object and RDR_object[0] and RDR_object[0].info_siteid:
                return RDR_object[0].info_siteid
        except RDRResource.DoesNotExist:
            pass
        return None

    def get_handle(self, ApplicationHandle):
        return({'HandleType': ApplicationHandle.Type,
                'HandleKey': ApplicationHandle.Value
               })
    
    def get_category(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension']['Category']
        except:
            return []

    def get_keywords(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Keywords']
        except:
            return []

    def get_supportstatus(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension']['SupportStatus']
        except:
            return []

    def get_supportcontact(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Extension']['SupportContact']
        except:
            return []

    def get_repository(self, ApplicationHandle):
        try:
            return ApplicationHandle.ApplicationEnvironment.EntityJSON['Repository']
        except:
            return []

class SGCI_Resource_Serializer_010(serializers.ModelSerializer):
    REMOVABLE_FIELDS = ['computeResources', 'storageResources', 'resourceOutages']
    schemaVersion = serializers.SerializerMethodField()
    host = serializers.CharField(source='info_resourceid')
    name = serializers.CharField(source='resource_descriptive_name')
    description = serializers.CharField(source='resource_description')
    computeResources = serializers.SerializerMethodField()
    storageResources = serializers.SerializerMethodField()
    resourceStatus = serializers.SerializerMethodField()
    resourceOutages = serializers.SerializerMethodField()
    class Meta:
        model = RDRResource
        fields = ('schemaVersion', 'host', 'name', 'description', 'computeResources', 'storageResources', 'resourceStatus', 'resourceOutages')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in self.REMOVABLE_FIELDS:
            try:
                if rep[field] is None:
                    rep.pop(field)
            except KeyError:
                pass
        return rep
        
    def get_schemaVersion(self, RDRResource):
        return('0.1.0')

    def get_computeResources(self, RDRResource):
        if RDRResource.rdr_type != 'compute':
            return(None)

        connections = []
        eps = Endpoint.objects.filter(ResourceID=RDRResource.info_resourceid)
        for ep in eps:
            if ep.InterfaceName == 'org.globus.openssh':
                for cp in ['SSH', 'SCP']:
                    for sp in ['SSHKEYS', 'X509']:
                        con = {'connectionProtocol': cp, 'securityProtocol': sp}
                        if ':' in ep.URL:
                            host, port = ep.URL.split(':')
                        else:
                            host, port = ep.URL, 22
                        if host == ep.ResourceID:
                            con['port'] = int(port) or 22
                        else:
                            con['proxyHost'] = host
                            con['proxyPort'] = int(port)
                        connections.append(con)
            elif ep.InterfaceName == 'org.globus.gridftp':
                con = {'connectionProtocol': 'GRIDFTP', 'securityProtocol': 'X509'}
                if ep.URL.startswith('gsiftp://'):
                    url = ep.URL[len('gsiftp://'):].rstrip('/')
                else:
                    url = ep.URL[:]
                if ':' in url:
                    host, port = url.split(':')
                else:
                    host, port = url, 2811
                if host == ep.ResourceID:
                    con['port'] = int(port) or 2811
                else:
                    con['proxyHost'] = host
                    con['proxyPort'] = int(port) or 2811
                connections.append(con)

        batchSystem = {}
        cm = ComputingManager.objects.filter(ResourceID=RDRResource.info_resourceid)
        if cm and cm[0].Name:
            batchSystem['jobManager'] = cm[0].Name
        else:
            batchSystem['jobManager'] = RDRResource.other_attributes.get('batch_system', 'N/A')

#        if RDRResource.info_resourceid == 'stampede2.tacc.xsede.org':
#            import pdb
#            pdb.set_trace()
            
        evs = ExecutionEnvironment.objects.filter(ResourceID=RDRResource.info_resourceid)
        partitions = []
        for ev in evs:
            totalNodes = ev.EntityJSON.get('TotalInstances')
            if not totalNodes:
                extension = ev.EntityJSON.get('Extension')
                if extension and extension.get('Nodes'):
                    totalNodes = len(extension.get('Nodes'))
            cpuCount = ev.EntityJSON.get('LogicalCPUs')
            par = {'name': ev.Name,
                    'nodehardware': {
                        'cpuType': ev.EntityJSON.get('Platform', 'n/a'),
                        'memorySize': ev.EntityJSON.get('MainMemorySize', 'n/a') }
                }
            if totalNodes:
                par['totalNodes'] = totalNodes
            if cpuCount:
                par['nodehardware']['cpuCount'] = cpuCount
            partitions.append(par)
        if partitions:
            batchSystem['partitions'] = partitions

        batch = {'schedulerType': 'BATCH'}
        if connections:
            batch['connections'] = connections
        if batchSystem:
            batch['batchSystem'] = batchSystem

        fork = {'schedulerType': 'FORK',
                'forkSystem': {'systemType': 'LINUX'}
            }
        if connections:
            fork['connections'] = connections

        result = [batch, fork]
        return(result)

    def get_storageResources(self, RDRResource):
        if RDRResource.rdr_type != 'storage':
            return(None)

        connections = []
        eps = Endpoint.objects.filter(ResourceID=RDRResource.info_resourceid)
        for ep in eps:
            if ep.InterfaceName == 'org.globus.openssh':
                for cp in ['SSH', 'SCP']:
                    for sp in ['SSHKEYS', 'X509']:
                        con = {'connectionProtocol': cp, 'securityProtocol': sp}
                        if ':' in ep.URL:
                            host, port = ep.URL.split(':')
                        else:
                            host, port = ep.URL, 22
                        if host == ep.ResourceID:
                            con['port'] = int(port) or 22
                        else:
                            con['proxyHost'] = host
                            con['proxyPort'] = int(port)
                        connections.append(con)
            elif ep.InterfaceName == 'org.globus.gridftp':
                con = {'connectionProtocol': 'GRIDFTP', 'securityProtocol': 'X509'}
                if ep.URL.startswith('gsiftp://'):
                    url = ep.URL[len('gsiftp://'):].rstrip('/')
                else:
                    url = ep.URL[:]
                if ':' in url:
                    host, port = url.split(':')
                else:
                    host, port = url, 2811
                if host == ep.ResourceID:
                    con['port'] = int(port) or 2811
                else:
                    con['proxyHost'] = host
                    con['proxyPort'] = int(port) or 2811
                connections.append(con)

        storage = {'storageType': 'POSIX'}
        if connections:
            storage['connections'] = connections

        result = [storage]
        return(result)

    def get_resourceStatus(self, RDRResource):
        status = {'status': RDRResource.latest_status.capitalize()}
        if RDRResource.latest_status_begin:
            status['starts'] = '{:%Y-%m-%d}'.format(RDRResource.latest_status_begin)
        if RDRResource.latest_status_end:
            status['ends'] = '{:%Y-%m-%d}'.format(RDRResource.latest_status_end)
        return(status)

    def get_resourceOutages(self, RDRResource):
        now = timezone.now()
        outages = []
        for out in Outages.objects.filter(ResourceID=RDRResource.info_resourceid, OutageStart__lte=now, OutageEnd__gte=now):
            item = {'type': out.OutageType.capitalize(),
                    'name': out.Subject,
                    'starts': out.OutageStart,
                    'ends': out.OutageEnd}
            if out.Content:
                item['description'] = out.Content
            if out.WebURL:
                item['url'] = out.WebURL
            outages.append(item)
        if outages:
            return(outages)
        else:
            return(None)
