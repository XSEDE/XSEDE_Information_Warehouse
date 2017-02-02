from xdinfo.models import *
from glue2_db.models import *
from glue2_db.serializers import *
from rest_framework import serializers
from pprint import pprint
import json

class xdinfo_service_Serializer(serializers.Serializer):
    
    ResourceID = serializers.CharField()
    URL = serializers.CharField()

class xdinfo_gram_Serializer(serializers.Serializer):
   
        Name = serializers.SerializerMethodField('get_jobmanager')
        URL = serializers.CharField()
        ResourceID = serializers.CharField()

        def get_jobmanager(self,Endpoint):
            try:
                jobmanager = Endpoint.URL.rsplit('-', 1)
            except Exception as err:
                returnstring = u"gram5-default"
            else:
                if len(jobmanager) == 2:
                    returnstring = u"gram5-"+jobmanager[1]
                else:
                    returnstring = u"gram5-default"
            return returnstring

class xdinfo_gridftps_Serializer(serializers.Serializer):
   
        Name = serializers.SerializerMethodField('get_striped')
        URL = serializers.CharField()
        ResourceID = serializers.CharField()

        def get_striped(self,Endpoint):
            return u"gridftp-striped-server"

class xdinfo_gridftpn_Serializer(serializers.Serializer):
   
        Name = serializers.SerializerMethodField('get_nonstriped')
        URL = serializers.CharField()
        ResourceID = serializers.CharField()

        def get_nonstriped(self,Endpoint):
            return u"gridftp-nonstriped-server"

class xdinfo_resource_Serializer(serializers.Serializer):
    
    info_resourceid = serializers.CharField()
    resource_descriptive_name = serializers.CharField()
    rdr_type = serializers.CharField()

class xdinfo_services_Serializer(serializers.Serializer):

    Type = serializers.SerializerMethodField('get_type')
    Name = serializers.CharField() 
    ResourceID = serializers.CharField()
    URL = serializers.CharField()

    def get_type(self,Endpoint):
        try:
            servicetype = Endpoint.Name.rsplit('.', 1)
        except Exception as err:
            returnstring = "unknown"
        else:
            if len(servicetype) > 1:
                returnstring = servicetype[1]
            else:
                returnstring = servicetype[0]
        return returnstring

class xdinfo_software_Serializer(serializers.Serializer):
   
    AppName = serializers.CharField() 
    AppVersion = serializers.CharField() 
    ResourceID = serializers.CharField()
    HandleType = serializers.SerializerMethodField('get_handle')
    Handlekey = serializers.SerializerMethodField('get_value')
    #Name = serializers.CharField()

    def get_handle(self,ApplicationEnvironment):
        #apphandleid in AppEnv is a _list_  We're going to punt and only consider the first element
        apphandleid = ApplicationEnvironment.EntityJSON['Associations']['ApplicationHandleID'][0]
        apphandlesearch = ApplicationHandle.objects.filter(ID=apphandleid)
        if apphandlesearch:
            apphandle = apphandlesearch[0]
#            print "printing apphandle\n"
#            pprint(apphandle)
#            pprint(apphandle.Type)
        else:
            return "unknown"
        return apphandle.Type

    def get_value(self,ApplicationEnvironment):
        #apphandleid in AppEnv is a _list_  We're going to punt and only consider the first element
        apphandleid = ApplicationEnvironment.EntityJSON['Associations']['ApplicationHandleID'][0]
        apphandlesearch = ApplicationHandle.objects.filter(ID=apphandleid)
        if apphandlesearch:
            apphandle = apphandlesearch[0]
        else:
            return "unknown"
        return apphandle.Value

class xdinfo_outage_Serializer(serializers.Serializer):
   
    SiteID = serializers.CharField()
    ResourceID = serializers.CharField()
    OutageStart = serializers.DateTimeField()
    OutageEnd = serializers.DateTimeField()
    Subject = serializers.CharField()


class xdinfo_sites_Serializer(serializers.Serializer):
   
    SiteID = serializers.CharField(source='info_siteid')
#    SiteID = serializers.CharField(source='info_resourceid')
#    OrganizationName = serializers.CharField(source='resource_descriptive_name')
