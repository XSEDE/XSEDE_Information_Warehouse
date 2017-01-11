import json
from datetime import datetime, tzinfo
from django.db import DataError, IntegrityError
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from glue2_db.models import *

from rest_framework import status
from xsede_warehouse.exceptions import ProcessingException

import pdb
import logging
logg2 = logging.getLogger('xsede.glue2')

Handled_Models = ('ApplicationEnvironment', 'ApplicationHandle', \
                  'AbstractService', 'Endpoint',
                  'ComputingManager', 'ComputingShare', 'ComputingActivity', \
                  'ExecutionEnvironment', 'Location', )

# Select Activity field cache
# New activities that match the cache aren't updated in the db to optimize performance
# The cache has a timestamp we can use to expire and reset the contents
a_cache = {}
a_cache_ts = timezone.now()

# The following class is under development and may replace StatsSummary
class StatsTracker():
    def __init__(self, Label):
        self.Label = Label
        self.ProcessingSeconds = 0
        for model in Handled_models:
            self.stats['%s.Updates' % model] = 0
            self.stats['%s.Deletes' % model] = 0
            self.stats['%s.ToCache' % model] = 0
    def __unicode__(self):
        out = 'Processed %s in %s/sec:' % (self.Label, str(self.ProcessingSeconds))
        for i in Handled_Models:
            if '%s.New' % i in self.stats and self.stats['%s.New' % i] > 0:
                out += ' %s %s->%s (%s/up, %s/del, %s/cache)' % \
                    (i, self.stats['%s.Current' % i], self.stats['%s.New' % i], self.stats['%s.Updates' % i], self.stats['%s.Deletes' % i], self.stats['%s.ToCache' % i])
        return(out)
    def HasApplication(self):
        return('ApplicationEnvironment.New' in self.stats or \
               'ApplicationHandle.New' in self.stats)
    
    def HasCompute(self):
        return ('AbstractService.New' in self.stats or \
                'Endpoint.New' in self.stats or \
                'ComputingManager.New' in self.stats or \
                'ExecutionEnvironment.New' in self.stats or \
                'Location.New' in self.stats or \
                'ComputingShare.New' in self.stats)
    def set(self, key, value):
        if key in self.stats:
            self.stats[key] = value
    def add(self, key, increment):
        if key in self.stats:
            self.stats[key] += value

def StatsSummary(stats):
    out = 'Processed %s in %s/sec:' % (stats['Label'], str(stats['ProcessingSeconds']))
    for i in Handled_Models:
        if '%s.New' % i in stats and stats['%s.New' % i] > 0:
            out += ' %s %s->%s (%s/up' % (i, stats['%s.Current' % i], stats['%s.New' % i], stats['%s.Updates' % i])
            if '%s.Deletes' % i in stats and stats['%s.Deletes' % i] > 0:
                out += ', %s/del' % stats['%s.Deletes' % i]
            if '%s.ToCache' % i in stats and stats['%s.ToCache' % i] > 0:
                out += ', %s/cache' % stats['%s.ToCache' % i]
            out += ')'
    return(out)

def StatsHadApplication(stats):
    return('ApplicationEnvironment.New' in stats or \
            'ApplicationHandle.New' in stats)

def StatsHadCompute(stats):
    return ('AbstractService.New' in stats or \
            'Endpoint.New' in stats or \
            'ComputingManager.New' in stats or \
            'ExecutionEnvironment.New' in stats or \
            'Location.New' in stats or \
            'ComputingShare.New' in stats)

def StatsHadServicesOnly(stats):
    return ( ('AbstractService.New' in stats or 'Endpoint.New' in stats) and
            'ComputingManager.New' not in stats and
            'ExecutionEnvironment.New' not in stats and
            'Location.New' not in stats and
            'ComputingShare.New' not in stats )

def StatsHadComputeActivity(stats):
    return('ComputingActivity.New' in stats)

# Create your models here.
class Glue2NewDocument():
    def __init__(self, DocType, ResourceID, ReceivedTime, Label):
        self.doctype = DocType
        self.resourceid = ResourceID
        self.receivedtime = ReceivedTime
        self.new = {}   # Contains new object json
        self.cur = {}   # Contains existing object references
        self.stats = { 'Label': Label, }
        for model in Handled_Models:
            self.new[model] = {}
            self.cur[model] = {}
            self.stats['%s.Updates' % model] = 0
            self.stats['%s.Deletes' % model] = 0
            self.stats['%s.ToCache' % model] = 0
        self.newAbsServType = {}

    def LoadNewEntityInstance(self, model, obj):
        if type(obj) is not list:
            raise ValidationError('New entity %s doesn\'t contain a list' % model)
        for item in obj:
            self.new[model][item['ID']] = item
        self.stats['%s.New' % model] = len(self.new[model])

###############################################################################################
# Application handling
###############################################################################################
    def ProcessApplication(self):
        ########################################################################
        me = 'ApplicationEnvironment'
        # Load current database entries
        for item in ApplicationEnvironment.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])
        
        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest
            try:
                other_json = self.new[me][ID].copy()
                for k in ['ID', 'Name', 'CreationTime', 'Description', 'AppName', 'AppVersion']:
                    other_json.pop(k, None)
                desc = self.new[me][ID].get('Description')
                if desc is not None:
                    desc = desc[:512]
                model = ApplicationEnvironment(ID=self.new[me][ID]['ID'],
                                               ResourceID=self.resourceid,
                                               Name=self.new[me][ID]['Name'],
                                               CreationTime=self.new[me][ID]['CreationTime'],
                                               Description=desc,
                                               AppName=self.new[me][ID]['AppName'],
                                               AppVersion=self.new[me][ID].get('AppVersion', 'none'),
                                               EntityJSON=other_json)
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
#       Temporary, perhaps permanent, warn of these types of errors but continue, 2016-10-20 JP
                logg2.warning('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message))
#                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
#                                          status=status.HTTP_400_BAD_REQUEST)

        ########################################################################
        me = 'ApplicationHandle'
        # Load current database entries
        for item in ApplicationHandle.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])
        
        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest
            try:
                fk = self.new['ApplicationEnvironment'][self.new[me][ID]['Associations']['ApplicationEnvironmentID']]['model']
            except:
                try:
                    fk = self.cur['ApplicationEnvironment'][self.new[me][ID]['Associations']['ApplicationEnvironmentID']]
                except:
                    fk = None
            try:
                other_json = self.new[me][ID].copy()
                for k in ['ID', 'Name', 'CreationTime', 'Type', 'Value']:
                    other_json.pop(k, None)
                model = ApplicationHandle(ID=self.new[me][ID]['ID'],
                                          ResourceID=self.resourceid,
                                          Name=self.new[me][ID]['Name'],
                                          CreationTime=self.new[me][ID]['CreationTime'],
                                          Type=self.new[me][ID]['Type'],
                                          Value=self.new[me][ID]['Value'],
                                          ApplicationEnvironment=fk,
                                          EntityJSON=other_json)
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
#       Temporary, perhaps permanent, warn of these types of errors but continue, 2016-10-20 JP
                logg2.warning('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message))
#                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
#                                          status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
        for ID in self.cur[me]:
            if ID in self.new[me]:
                continue
            try:
                ApplicationEnvironment.objects.filter(ID=ID).delete()
                self.stats['%s.Deletes' % me] += 1
            except (DataError, IntegrityError) as e:
#       Temporary, perhaps permanent, warn of these types of errors but continue, 2016-10-20 JP
                logg2.warning('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message))
#                raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
#                                          status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
        me = 'ApplicationEnvironment'
        for ID in self.cur[me]:
            if ID in self.new[me]:
                continue
            try:
                ApplicationEnvironment.objects.filter(ID=ID).delete()
                self.stats['%s.Deletes' % me] += 1
            except (DataError, IntegrityError) as e:
#       Temporary, perhaps permanent, warn of these types of errors but continue, 2016-10-20 JP
                logg2.warning('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message))
#               raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
#                                          status=status.HTTP_400_BAD_REQUEST)

###############################################################################################
# Compute handling
###############################################################################################
    def LoadNewAbstractService(self, model, obj):
        if type(obj) is not list:
            raise ValidationError('New AbstractService(%s) doesn\'t contain a list' % model)
        for item in obj:
            self.new['AbstractService'][item['ID']] = item
            self.newAbsServType[item['ID']] = model
        self.stats['AbstractService.New'] = len(self.new['AbstractService'])

    def ProcessCompute(self):
        ########################################################################
        me = 'AbstractService'
        ServicesOnly = StatsHadServicesOnly(self.stats)
        # Load current database entries
        for item in AbstractService.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])
        
        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest
            try:
                other_json = self.new[me][ID].copy()
                for k in ['ID', 'Name', 'CreationTime', 'Type', 'QualityLevel']:
                    other_json.pop(k, None)
                model = AbstractService(ID=self.new[me][ID]['ID'],
                                        ResourceID=self.resourceid,
                                        Name=self.new[me][ID]['Name'],
                                        CreationTime=self.new[me][ID]['CreationTime'],
                                        EntityJSON=other_json,
                                        ServiceType=self.newAbsServType[ID],
                                        Type=self.new[me][ID]['Type'],
                                        QualityLevel=self.new[me][ID].get('QualityLevel', 'none'))
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        ########################################################################
        me = 'Endpoint'
        # Load current database entries
        for item in Endpoint.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])
        
        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest
            try:
                fk = self.new['AbstractService'][self.new[me][ID]['Associations']['ServiceID']]['model']
            except:
                try:
                    fk = self.cur['AbstractService'][self.new[me][ID]['Associations']['ServiceID']]
                except:
                    raise ProcessingException('Missing ServiceID FK', status=status.HTTP_400_BAD_REQUEST)
            try:
                other_json = self.new[me][ID].copy()
                for k in ['ID', 'Name', 'CreationTime', 'HealthState', 'ServingState', 'URL',
                          'QualityLevel', 'InterfaceVersion', 'InterfaceName']:
                    other_json.pop(k, None)
                model = Endpoint(ID=self.new[me][ID]['ID'],
                                 ResourceID=self.resourceid,
                                 Name=self.new[me][ID]['Name'],
                                 CreationTime=self.new[me][ID]['CreationTime'],
                                 AbstractService=fk,
                                 EntityJSON=other_json,
                                 HealthState=self.new[me][ID]['HealthState'],
                                 ServingState=self.new[me][ID]['ServingState'],
                                 URL=self.new[me][ID]['URL'],
                                 QualityLevel=self.new[me][ID].get('QualityLevel', 'none'),
                                 InterfaceVersion=self.new[me][ID]['InterfaceVersion'],
                                 InterfaceName=self.new[me][ID]['InterfaceName'],)
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
# 2016-01-28 JP: TEMPORARY BECAUSE SERVICES COME IN TWO WAYS ONE SHOULDN'T DELETE OTHER
#        for ID in self.cur[me]:
#            if ID in self.new[me]:
#                continue
#            try:
#                Endpoint.objects.filter(ID=ID).delete()
#                self.stats['%s.Deletes' % me] += 1
#            except (DataError, IntegrityError) as e:
#                raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
#                                          status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
# 2016-01-28 JP: TEMPORARY BECAUSE SERVICES COME IN TWO WAYS ONE SHOULDN'T DELETE OTHER
#        me = 'AbstractService'
#        for ID in self.cur[me]:
#            if ID in self.new[me]:
#                continue
#            try:
#                AbstractService.objects.filter(ID=ID).delete()
#                self.stats['%s.Deletes' % me] += 1
#            except (DataError, IntegrityError) as e:
#                raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
#                                          status=status.HTTP_400_BAD_REQUEST)

        ########################################################################
        me = 'ComputingManager'
        # Load current database entries
        for item in ComputingManager.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])
        
        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest
            try:
                model = ComputingManager(ID=self.new[me][ID]['ID'],
                                          ResourceID=self.resourceid,
                                          Name=self.new[me][ID]['Name'],
                                          CreationTime=self.new[me][ID]['CreationTime'],
                                          EntityJSON=self.new[me][ID])
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
        for ID in self.cur[me]:
            if ID in self.new[me]:
                continue
            try:
                ComputingManager.objects.filter(ID=ID).delete()
                self.stats['%s.Deletes' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        ########################################################################
        me = 'ExecutionEnvironment'
        # Load current database entries
        for item in ExecutionEnvironment.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])

        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest
            try:
                model = ExecutionEnvironment(ID=self.new[me][ID]['ID'],
                                          ResourceID=self.resourceid,
                                          Name=self.new[me][ID]['Name'],
                                          CreationTime=self.new[me][ID]['CreationTime'],
                                          EntityJSON=self.new[me][ID])
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
        for ID in self.cur[me]:
            if ID in self.new[me]:
                continue
            try:
                ExecutionEnvironment.objects.filter(ID=ID).delete()
                self.stats['%s.Deletes' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        ########################################################################
        me = 'Location'
        # Load current database entries
        for item in Location.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])
        
        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest
            try:
                model = Location(ID=self.new[me][ID]['ID'],
                                          ResourceID=self.resourceid,
                                          Name=self.new[me][ID]['Name'],
                                          CreationTime=self.new[me][ID]['CreationTime'],
                                          EntityJSON=self.new[me][ID])
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
        for ID in self.cur[me]:
            if ID in self.new[me]:
                continue
            try:
                Location.objects.filter(ID=ID).delete()
                self.stats['%s.Deletes' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        ########################################################################
        me = 'ComputingShare'
        # Load current database entries
        for item in ComputingShare.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])
        
        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest
            try:
                model = ComputingShare(ID=self.new[me][ID]['ID'],
                                          ResourceID=self.resourceid,
                                          Name=self.new[me][ID]['Name'],
                                          CreationTime=self.new[me][ID]['CreationTime'],
                                          EntityJSON=self.new[me][ID])
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
        for ID in self.cur[me]:
            if ID in self.new[me]:
                continue
            try:
                ComputingShare.objects.filter(ID=ID).delete()
                self.stats['%s.Deletes' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

###############################################################################################
# ComputingActivity handling
###############################################################################################
    def ProcessComputingActivity(self):
        ########################################################################
        me = 'ComputingActivity'
#        pdb.set_trace()
        # Load current database entries
        for item in ComputingActivity.objects.filter(ResourceID=self.resourceid):
            self.cur[me][item.ID] = item
        self.stats['%s.Current' % me] = len(self.cur[me])
        
        # Add/update entries
        for ID in self.new[me]:
            if ID in self.cur[me] and parse_datetime(self.new[me][ID]['CreationTime']) <= self.cur[me][ID].CreationTime:
                self.new[me][ID]['model'] = self.cur[me][ID]    # Save the latest object reference
                continue                                        # Don't update database since is has the latest

            if self.activity_is_cached(ID, self.new[me][ID]):
                self.stats['%s.ToCache' % me] += 1
                continue
            
            try:
                model = ComputingActivity(ID=self.new[me][ID]['ID'],
                                          ResourceID=self.resourceid,
                                          Name=self.new[me][ID].get('Name', 'none'),
                                          CreationTime=self.new[me][ID]['CreationTime'],
                                          EntityJSON=self.new[me][ID])                                          
                model.save()
                self.new[me][ID]['model'] = model
                self.stats['%s.Updates' % me] += 1
                
                self.activity_to_cache(ID, self.new[me][ID])
            
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], \
                                        e.message), status=status.HTTP_400_BAD_REQUEST)

        # Delete old entries
        for ID in self.cur[me]:
            if ID in self.new[me]:
                continue
            try:
                ComputingActivity.objects.filter(ID=ID).delete()
                self.stats['%s.Deletes' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s deleting %s (ID=%s): %s' % (type(e).__name__, me, ID, e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

    def activity_is_cached(self, id, obj): # id=object unique id
        global a_cache
        global a_cache_ts
        if (timezone.now() - a_cache_ts).total_seconds() > 3600:    # Expire cache every hour (3600 seconds)
            a_cache_ts = timezone.now()
            a_cache = {}
            logg2.debug('Expiring Activity cache')

        return id in a_cache and a_cache[id] == self.activity_hash(obj)

    def activity_to_cache(self, id, obj):
        global a_cache
        a_cache[id] = self.activity_hash(obj)
    
    def activity_hash(self, obj):
        hash_list = []
        if 'State' in obj:
            hash_list.append(obj['State'])
        if 'UsedTotalWallTime' in obj:
            hash_list.append(obj['UsedTotalWallTime'])
        return(json.dumps(hash_list))
    
###############################################################################################
# Main code to Load New JSON objects and Process each class of objects
###############################################################################################
    handlers = {'ApplicationHandle': LoadNewEntityInstance,
                'ApplicationEnvironment': LoadNewEntityInstance,
                'ComputingService': LoadNewAbstractService,
                'InformationService': LoadNewAbstractService,
                'LoginService': LoadNewAbstractService,
                'StorageService': LoadNewAbstractService,
                'UntypedService': LoadNewAbstractService,
                'Endpoint': LoadNewEntityInstance,
                'ComputingManager': LoadNewEntityInstance,
                'ExecutionEnvironment': LoadNewEntityInstance,
                'Location': LoadNewEntityInstance,
                'ComputingShare': LoadNewEntityInstance,
                'ComputingActivity': LoadNewEntityInstance,
    }
    
    def process(self, data):
        if type(data) is not dict:
            msg = 'Expecting a JSON dictionary (DocType=%s, ResourceID=%s, ReceivedTime=%s)' % \
                (self.doctype, self.resourceid, self.receivedtime)
            logg2.error(msg)
            raise ValidationError(msg)
        start = datetime.utcnow()
        for key in data:
            if key in self.handlers:
                self.handlers[key](self, key, data[key])
            else:
                logg2.warning('Element "%" not recognized (DocType=%s, ResourceID=%s, ReceivedTime=%s)' % \
                              (key, self.doctype, self.resourceid, str(self.receivedtime)))
        if StatsHadApplication(self.stats):
            self.ProcessApplication()
        elif StatsHadCompute(self.stats):
            self.ProcessCompute()
        elif StatsHadComputeActivity(self.stats):
            self.ProcessComputingActivity()

        end = datetime.utcnow()
        self.stats['ProcessingSeconds'] = (end - start).total_seconds()
        logg2.info(StatsSummary(self.stats))
        return(self.stats)