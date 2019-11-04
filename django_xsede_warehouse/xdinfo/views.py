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

    def get_version(self):
        version = '1'
        return('API version {}'.format(version))

    def get(self, request, format=None, **kwargs):
        #print self.kwargs
        infoformat = self.kwargs.get('infoformat', 'csv')

        # Map of valid input types and corresponding canonical types
        # The rest of this application is driven by the canonical type
        infotype_map = {
            'help':         'help',
            'briefhelp':    'briefhelp',
            'version':      'version',
            'gram5':        'gram5',
            'gram':         'gram5',
            'gridftp':      'gridftp',
            'login':        'login',
            'ssh':          'login',
            'resources':    'resources',
            'res':          'resources',
            'services':     'services',
            'serv':         'services',
            'software':     'software',
            'soft':         'software',
            'outages':      'outages',
            'out':          'outages',
            'sites':        'sites'
        }
        # If there is no infotype default to briefhelp
        infotype = self.kwargs.get('infotype', 'briefhelp').lower()
        try: # Translate to canonical
            infotype = infotype_map[infotype]
        except:
            return HttpResponse('Unknown option "{}"'.format(infotype), content_type="text/plain")

        if infotype == 'help':
            return HttpResponse(self.get_helptext(False), content_type="text/plain")
        if infotype == 'briefhelp':
            return HttpResponse(self.get_helptext(True), content_type="text/plain")
        if infotype == 'version':
            return HttpResponse(self.get_version(), content_type="text/plain")

        now = timezone.now()
        if 'slug' in self.kwargs:
            #print self.kwargs['slug']
            arglist = self.kwargs['slug'].split('/')
            #print arglist
        else:
            arglist = ()
        noheaderflag = 'noheader' in arglist
        if noheaderflag:
            arglist.remove('noheader')

        if infotype == 'outages':
            allflag = False
            currentflag = False
            recentflag = False
            pastflag = False
            futureflag = False
            if 'all' in arglist:
                allflag = True
                arglist.remove('all')
            elif 'current' in arglist:
                currentflag = True
                arglist.remove('current')
            elif 'recent' in arglist:
                recentflag = True
                arglist.remove('recent')
            elif 'past' in arglist:
                pastflag = True
                arglist.remove('past')
            elif 'future' in arglist:
                futureflag = True
                arglist.remove('future')

        # Handle the "at" or "on" qualifier
        aton_index = None
        aton_string = ''
        if 'at' in arglist:
            aton_index = arglist.index('at')
            arglist.remove('at')
        elif 'on' in arglist:
            aton_index = arglist.index('on')
            arglist.remove('on')
        if aton_index is not None:
            if (aton_index + 1) > len(arglist):
                return HttpResponse('The at/on option is missing a <match_string>', content_type="text/plain")
            aton_string = arglist.pop(aton_index) # Because we removed at/on, the string should be in the same position

        filter_string = ''
        if arglist:
            filter_string = arglist[0]

        if infotype == 'gridftp':
            if aton_string:
                objects = Endpoint.objects.filter(AbstractService__EntityJSON__Capability__contains=['data.transfer.nonstriped']).filter(ResourceID__icontains=aton_string)
                serializernonstriped = xdinfo_gridftpn_Serializer(objects, many=True)
                objects = Endpoint.objects.filter(AbstractService__EntityJSON__Capability__contains=['data.transfer.striped']).filter(ResourceID__icontains=aton_string)
                serializerstriped = xdinfo_gridftps_Serializer(objects, many=True)
            else:
                objects = Endpoint.objects.filter(AbstractService__EntityJSON__Capability__contains=['data.transfer.nonstriped'])
                serializernonstriped = xdinfo_gridftpn_Serializer(objects, many=True)
                objects = Endpoint.objects.filter(AbstractService__EntityJSON__Capability__contains=['data.transfer.striped'])
                serializerstriped = xdinfo_gridftps_Serializer(objects, many=True)
            serialized_data = serializerstriped.data+serializernonstriped.data
        else:
            casedict = {
                'gram5':{   'objects':      Endpoint.objects,
                            'filter_dict':  {'Name__exact': 'org.globus.gram'},
                            'resid_field':  'ResourceID__icontains',
                            'match_field':  'URL__icontains',
                            'serializer':   xdinfo_gram_Serializer},
                'login':{   'objects':      Endpoint.objects,
                            'filter_dict': {'Name__exact': 'org.globus.openssh'},
                            'resid_field':  'ResourceID__icontains',
                            'match_field':  'URL__icontains',
                            'serializer':   xdinfo_service_Serializer},
                'resources':{'objects':     RDRResource.objects,
                            'filter_dict': {'current_statuses__exact': 'production'},
                            'resid_field':  'info_resourceid__contains',
                            'match_field':  'resource_descriptive_name__icontains',
                            'serializer':   xdinfo_resource_Serializer},
                'services':{'objects':      Endpoint.objects,
                            'filter_dict': {'ServingState__exact': 'production'},
                            'resid_field':  'ResourceID__icontains',
                            'match_field':  'URL__icontains',
                            'serializer':   xdinfo_services_Serializer},
                'software':{'objects':      ApplicationEnvironment.objects,
                            'filter_dict': {},
                            'resid_field':  'ResourceID__icontains',
                            'match_field':  'AppName__icontains',
                            'serializer':   xdinfo_software_Serializer},
                'outages':{ 'objects':      Outages.objects,
                            'filter_dict': {'OutageStart__lte': now,
                                            'OutageEnd__gte': now},
                            'resid_field':  'ResourceID__icontains',
                            'match_field':  'Subject__icontains',
                            'serializer':   xdinfo_outage_Serializer},
                'sites':{   'objects':      RDRResource.objects.values('info_siteid').distinct(),
                            'filter_dict': {'rdr_type__in': ['compute','storage']},
                            'resid_field':  'info_siteid__contains',
                            'match_field':  'resource_descriptive_name__icontains',
                            'serializer':   xdinfo_sites_Serializer},
            }

            my_filter_dict = casedict[infotype]['filter_dict']
            if infotype == 'outages':
                if pastflag:
                    my_filter_dict['OutageEnd__lte'] = my_filter_dict.pop('OutageEnd__gte')
                if futureflag:
                    my_filter_dict['OutageStart__gte'] = my_filter_dict.pop('OutageStart__lte')
                if recentflag:
                    my_filter_dict['OutageEnd__range'] = [now - datetime.timedelta(7), now]
                    my_filter_dict.pop('OutageEnd__gte')
                if allflag:
                    my_filter_dict.pop('OutageEnd__gte')
                    my_filter_dict.pop('OutageStart__lte')
            if aton_string:
                my_filter_dict[casedict[infotype]['resid_field']] = aton_string
            if filter_string:
                my_filter_dict[casedict[infotype]['match_field']] = filter_string

            #print my_filter_dict
            objects = casedict[infotype]['objects'].filter(**my_filter_dict)
            #print objects
            serializer = casedict[infotype]['serializer'](objects, many=True)
            #serializer = casedict[infotype]['serializer'](objects, many=True,context={'aton_string': serializerarg})
            serialized_data = serializer.data

        returnstring = ''
        headerstring = ''
        width = {}
        #calculate maximum width of key/value for formatting
        if infoformat != 'csv':
            for line in serialized_data:
                #print line
                for key, value in line.items():
                    # Replace during Python 3 upgrade
#                    keylen = len(key.decode("utf-8"))
#                    vallen = len(unicodedata.normalize('NFC', safe_unicode(value)))
                    keylen = len(key)
                    vallen = len(unicodedata.normalize('NFC', value))
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
                    # Replace during Python 3 upgrade
#                    fmtstring = '{:'+unicode(width[key]+1)+'}'
                    fmtstring = '{:'+str(width[key]+1)+'}'
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

        if noheaderflag:
            return HttpResponse(returnstring, content_type="text/plain")
        else:
            return HttpResponse(headerstring+returnstring, content_type="text/plain")

    def get_helptext(self, brief):
        #brief = False;
        helpstring = """XSEDE Information Services Discovery Client ({})

""".format(self.get_version())
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

# Deprecated during Python 3 upgrade
#def safe_unicode(obj, *args):
#    """ return the unicode representation of obj """
#    try:
#        return unicode(obj, *args)
#    except UnicodeDecodeError:
#        # obj is byte string
#        ascii_text = str(obj).encode('string_escape')
#        return unicode(ascii_text)
