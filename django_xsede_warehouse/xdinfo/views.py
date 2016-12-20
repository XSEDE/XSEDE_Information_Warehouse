from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from xdinfo.models import *
from xdinfo.serializers import *
from glue2_db.models import *
from glue2_db.serializers import *
from rdr_db.models import *
from rdr_db.serializers import *
from goendpoint_api.serializers import *
from outages.models import *
from itertools import chain
import datetime
import unicodedata
#import kitchen.text.converters

# Create your views here.

class xdinfo_Cmd(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None, **kwargs):
        #print self.kwargs
        pastflag = False
        futureflag = False
        currentflag = False
        recentflag = False
        allflag = False
        headerflag = True
        arg1 = None
        infoformat = 'csv'
        #If we've come in with only one kwarg, it is the infoformat
        #which means that the command line had no args, so display briefhelp
        if len(self.kwargs.keys()) == 1:
            return HttpResponse(self.get_helptext(True), content_type="text/plain")
        if 'infoformat' in self.kwargs:
            infoformat = self.kwargs['infoformat']
        if 'infotype' in self.kwargs:
          if self.kwargs['infotype'] == "help":
            return HttpResponse(self.get_helptext(False), content_type="text/plain")
          if self.kwargs['infotype'] == "briefhelp":
            return HttpResponse(self.get_helptext(True), content_type="text/plain")
          if self.kwargs['infotype'] == "version":
            return HttpResponse("API version 1", content_type="text/plain")
          now = timezone.now()
          if 'slug' in self.kwargs:
            #print self.kwargs['slug']
            arglist = self.kwargs['slug'].split('/')
            if 'at' in arglist:
                arglist.remove('at')
            if 'on' in arglist:
                arglist.remove('on')
            #print arglist
            if 'current' in arglist:
                currentflag = True
                arglist.remove('current')
            if 'recent' in arglist:
                recentflag = True
                arglist.remove('recent')
            if 'past' in arglist:
                pastflag = True
                arglist.remove('past')
            if 'future' in arglist:
                futureflag = True
                arglist.remove('future')
            if 'all' in arglist:
                allflag = True
                arglist.remove('all')
            if 'noheader' in arglist:
                headerflag = False
                arglist.remove('noheader')
            if arglist:
                arg1 = arglist[0]
          if self.kwargs['infotype'] == "gridftp":
             if arg1:
                objects = Endpoint.objects.filter(AbstractService__EntityJSON__Capability__contains=['data.transfer.nonstriped']).filter(ResourceID__icontains=arg1)
                serializernonstriped = xdinfo_gridftpn_Serializer(objects,many=True)
                objects = Endpoint.objects.filter(AbstractService__EntityJSON__Capability__contains=['data.transfer.striped']).filter(ResourceID__icontains=arg1)
                serializerstriped = xdinfo_gridftps_Serializer(objects,many=True)
             else:
                objects = Endpoint.objects.filter(AbstractService__EntityJSON__Capability__contains=['data.transfer.nonstriped'])
                serializernonstriped = xdinfo_gridftpn_Serializer(objects,many=True)
                objects = Endpoint.objects.filter(AbstractService__EntityJSON__Capability__contains=['data.transfer.striped'])
                serializerstriped = xdinfo_gridftps_Serializer(objects,many=True)
             serialized_data = serializerstriped.data+serializernonstriped.data
          else:
            filter_dict = {}
            casedict = {
                'gram5':{'objects': Endpoint.objects,
                            'filter_dict': {'Name__exact': 'org.globus.gram'},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_gram_Serializer},
                'gram':{'objects': Endpoint.objects,
                            'filter_dict': {'Name__exact': 'org.globus.gram'},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_gram_Serializer},
                'login':{'objects': Endpoint.objects,
                            'filter_dict': {'Name__exact': 'org.globus.openssh'},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_service_Serializer},
                'ssh':{'objects': Endpoint.objects,
                            'filter_dict': {'Name__exact': 'org.globus.openssh'},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_service_Serializer},
                'res':{'objects': RDRResource.objects,
                            'filter_dict': {'current_statuses__exact': 'production'},
                            'arg1_filter': 'info_resourceid__contains',
                            'serializer': xdinfo_resource_Serializer},
                'resources':{'objects': RDRResource.objects,
                            'filter_dict': {'current_statuses__exact': 'production'},
                            'arg1_filter': 'info_resourceid__contains',
                            'serializer': xdinfo_resource_Serializer},
                'serv':{'objects': Endpoint.objects,
                            'filter_dict': {'ServingState__exact': 'production'},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_services_Serializer},
                'services':{'objects': Endpoint.objects,
                            'filter_dict': {'ServingState__exact': 'production'},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_services_Serializer},
                'soft':{'objects': ApplicationEnvironment.objects,
                            'filter_dict': {},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_software_Serializer},
                'software':{'objects': ApplicationEnvironment.objects,
                            'filter_dict': {},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_software_Serializer},
                'out':{'objects': Outages.objects,
                            'filter_dict': {'OutageStart__lte': now,
                                            'OutageEnd__gte': now},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_outage_Serializer},
                'outages':{'objects': Outages.objects,
                            'filter_dict': {'OutageStart__lte': now,
                                            'OutageEnd__gte': now},
                            'arg1_filter': 'ResourceID__icontains',
                            'serializer': xdinfo_outage_Serializer},
                'sites':{'objects': RDRResource.objects,
                            'filter_dict': {'rdr_type__in': ['compute','storage']},
                            'arg1_filter': 'info_resourceid__contains',
                            'serializer': xdinfo_sites_Serializer},
            }

            if self.kwargs['infotype'] not in set().union(casedict.keys(),['gridftp','outages','out']):
                returnstring = "Unknown option %s" %self.kwargs['infotype']
                return HttpResponse(returnstring, content_type="text/plain")

            filter_dict = casedict[self.kwargs['infotype']]['filter_dict']

            if self.kwargs['infotype'] == 'outages' or self.kwargs['infotype'] =='out':
                if pastflag:
                    filter_dict['OutageEnd__lte'] = filter_dict.pop('OutageEnd__gte')
                if futureflag:
                    filter_dict['OutageStart__gte'] = filter_dict.pop('OutageStart__lte')
                if recentflag:
                    filter_dict['OutageEnd__range'] = [now - datetime.timedelta(7), now]
                    filter_dict.pop('OutageEnd__gte')
                    #filter_dict.pop('OutageStart__Lte')
                if allflag:
                    filter_dict.pop('OutageEnd__gte')
                    filter_dict.pop('OutageStart__lte')
            if arg1:
                filter_dict[casedict[self.kwargs['infotype']]['arg1_filter']]= arg1
            #print filter_dict
            objects = casedict[self.kwargs['infotype']]['objects'].filter(**filter_dict)
            #print objects
            serializer = casedict[self.kwargs['infotype']]['serializer'](objects, many=True)
            #serializer = casedict[self.kwargs['infotype']]['serializer'](objects, many=True,context={'arg1': serializerarg})
            serialized_data = serializer.data

          returnstring = ''
          headerstring = ''
          width = {}
          #calculate maximum width of key/value for formatting
          if infoformat != 'csv':
            for line in serialized_data:
                #print line
                for key, value in line.items():
                    keylen = len(key.decode("utf-8"))
                    vallen = len(unicodedata.normalize('NFC', safe_unicode(value)))
                    #This was working except for non-mappable unicode chars
                    #vallen = len(value.decode("utf-8"))
                        
                    if not key in width:
                        width[key]=0;
                    if vallen > width[key]:
                        width[key] = vallen
                    if keylen > width[key]:
                        width[key] = keylen

            for line in serialized_data:
                #print line
                headerstring = ''
                for key, value in line.items():
                    fmtstring = '{:'+unicode(width[key]+1)+'}'
                    returnstring += fmtstring.format(value)
                    headerstring += fmtstring.format(key)
                returnstring += "\n"
                headerstring += "\n"
          else:
            for line in serialized_data:
                #print line
                headerstring = ''
                for key, value in line.items():
                    returnstring += value+u","
                    headerstring += key+u","
                if returnstring.endswith(","): returnstring = returnstring[:-1]
                if headerstring.endswith(","): headerstring = headerstring[:-1]

                returnstring += "\n"
                headerstring += "\n"

        if not headerflag:
            return HttpResponse(returnstring, content_type="text/plain")
        else:
            return HttpResponse(headerstring+returnstring, content_type="text/plain")

    def get_helptext(self,brief):
        #brief = False;
        helpstring = """XSEDE Information Services Discovery Client (API Version 1)

"""
        if (not brief):
            helpstring += """Syntax: xdinfo <information_type> [<match_string>] [options]
""" 
        helpstring += """Information types:
  gridftp|login|ssh              List these services
  gram|gram5                     List these services
"""
        if (not brief):
            helpstring += """  sites       [<match_string>]   List sites
"""
        helpstring += """  res[ources] [<match_string>]   List resources
  serv[ices]  [<match_string>]   List services
  soft[ware]  [<match_string>]   List software
  out[ages]   [<match_string>]   List outages
  help                           Show all help information
"""
        if (not brief):
            helpstring += """  briefhelp                      Show brief help information
"""
        helpstring += """  version                        Show tginfo version
"""
        if (not brief):
            helpstring += """Option modifiers:

  at           <match_string>    Show information at matching site
  on           <match_string>    Show information on matching resources
  local                          Show information for local resource
  global                         Show information for all resource
  noheader                       Do not print column headers
  current/recent/future/all      For outages only

Additional documentation available at https://software.xsede.org/production/xdinfo/latest/User_Documentation.html"""

        return helpstring

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)
