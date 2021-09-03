import json
from datetime import datetime, tzinfo, timedelta
from django.utils import timezone
from django.db import DataError, IntegrityError
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from monitoring_db.models import *
from glue2_db.models import *

from processing_status.process import ProcessingActivity
from xsede_warehouse.exceptions import ProcessingException

import logging
logg2 = logging.getLogger('xsede.logger')

Handled_Models = ('TestResult', )

def StatsSummary(stats):
    out = 'Processed %s in %s/sec:' % (stats['Label'], str(stats['ProcessingSeconds']))
    for i in Handled_Models:
        if '%s.New' % i in stats and stats['%s.New' % i] > 0:
            out += ' %s %s->%s (%s/up, %s/del)' % \
                (i, stats['%s.Current' % i], stats['%s.New' % i], stats['%s.Updates' % i], stats['%s.Deletes' % i])
    return(out)

def StatsHadTestResult(stats):
    return('TestResult.New' in stats)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return 'UTC'
    def dst(self, dt):
        return timedelta(0)
utc = UTC()

class Glue2NewMonitoring():
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
        self.newAbsServType = {}

    def LoadNewMonitoringService(self, model, obj):
        if type(obj) is not dict:
            logg2.error('New entity %s doesn\'t contain a dictionary' % model)
#            raise ValidationError('New entity %s doesn\'t contain a dictionary' % model)
            return
        if 'ID' not in obj:
            logg2.error('New entity %s is missing the ID attribute' % model)
#            raise ValidationError('New entity %s is missing the ID attribute' % model)
            return

        self.new[model][obj['ID']] = obj
        self.stats['%s.New' % model] = len(self.new[model])

###############################################################################################
# TestResult handling
###############################################################################################
    def ProcessTestResult(self):
        ########################################################################
        me = 'TestResult'
        # Add/update entries
        self.stats['%s.Current' % me] = 0
        for ID in self.new[me]:
            extension = self.new[me][ID]['Extension']
            associations = self.new[me][ID]['Associations']
            issoftware = False
            isservice = False
            errormessage = None

            try:
                if associations['SoftwareID']:
                    issoftware = True
            except KeyError:
                issoftware = False
            try:
                if associations['ServiceID']:
                    isservice = True
            except KeyError:
                isservice = False

            maxmsg = TestResult._meta.get_field('ErrorMessage').max_length
            if 'ErrorMessage' not in extension:
                errormessage = None
            elif len(extension['ErrorMessage']) > maxmsg:
                errormessage = extension['ErrorMessage'][:maxmsg]
                logg2.error('Truncated ErrorMessage to %s bytes, ID=%s' % (maxmsg, ID))
            else:
                errormessage = extension['ErrorMessage']

            logg2.debug('ID=%s, ResourceID=%s, Name=%s' % (self.new[me][ID]['ID'], self.resourceid, self.new[me][ID]['Name']))

            try:
                nagios_m, created = TestResult.objects.get_or_create(ID=self.new[me][ID]['ID'], defaults={
                                                                    "ResourceID": self.resourceid,
                                                                    "Name": self.new[me][ID]['Name'],
                                                                    "CreationTime": self.new[me][ID]['CreationTime'],
                                                                    "EntityJSON": self.new[me][ID],
                                                                    "Source": extension['Source'].lower(),
                                                                    "Result": extension['Result'].lower(),
                                                                    "ErrorMessage": errormessage,
                                                                    "IsSoftware" : issoftware,
                                                                    "IsService": isservice
                                                                     })
                if not created:
                    self.stats['%s.Current' % me] = 1
                    if parse_datetime(self.new[me][ID]['CreationTime']) > nagios_m.CreationTime:
                        TestResult.objects.filter(ID=self.new[me][ID]['ID']).update(ResourceID=self.resourceid,
                                                                             Name=self.new[me][ID]['Name'],
                                                                             CreationTime=self.new[me][ID]['CreationTime'],
                                                                             EntityJSON=self.new[me][ID],
                                                                             Source=extension['Source'].lower(),
                                                                             Result=extension['Result'].lower(),
                                                                             ErrorMessage=errormessage,
                                                                             IsSoftware=issoftware,
                                                                             IsService=isservice)
                self.new[me][ID]['model'] = nagios_m
                self.stats['%s.Updates' % me] += 1
            except (DataError, IntegrityError) as e:
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message))

###############################################################################################
# Main code to Load New JSON objects and Process each class of objects
###############################################################################################
    handlers = {
                'TestResult': LoadNewMonitoringService,
    }

    def process(self, data):
        if type(data) is not dict:
            msg = 'Expecting a JSON dictionary (DocType=%s, ResourceID=%s, ReceivedTime=%s)' % \
                (self.doctype, self.resourceid, self.receivedtime)
            logg2.error(msg)
            raise ValidationError(message=msg)
        start = datetime.utcnow()
        for key in data:
            if key in self.handlers:
                self.handlers[key](self, key, data[key])
            else:
                logg2.warning('Element "%s" not recognized (DocType=%s, ResourceID=%s, ReceivedTime=%s)' % \
                              (key, self.doctype, self.resourceid, str(self.receivedtime)))
        if StatsHadTestResult(self.stats):
            self.ProcessTestResult()

        end = datetime.utcnow()
        self.stats['ProcessingSeconds'] = (end - start).total_seconds()
        logg2.info(StatsSummary(self.stats))
        return(self.stats)

class Glue2ProcessRawMonitoring():
    def __init__(self, application='n/a', function='n/a'):
        self.application = application
        self.function = function

    def process(self, ts, doctype, resourceid, rawdata):
        # Return an error message, or nothing
        if doctype not in ['inca','nagios']:
            msg = 'Ignoring DocType (DocType={}, ResourceID={})'.format(doctype, resourceid)
            logg2.info(msg)
            return (False, msg)

        pa_id = '{}:{}'.format(doctype, resourceid)
        pa = ProcessingActivity(self.application, self.function, pa_id, doctype, resourceid)

        if isinstance(rawdata, dict):
            jsondata = rawdata
        else:
            try:
                jsondata = json.loads(rawdata)
            except:
                msg = 'Failed JSON parse (DocType={}, ResourceID={}, size={})'.format(doctype, resourceid, len(rawdata))
                logg2.error(msg)
                pa.FinishActivity('1', msg)
                return (False, msg)
        
        if doctype == 'inca' and 'rep:report' in jsondata:
            msg = 'Ignored legacy rep:report (DocType={}, ResourceID={})'.format(doctype, resourceid)
            logg2.info(msg)
            pa.FinishActivity(False, msg)
            return (False, msg)

        try:
            internal_resourceid = jsondata['TestResult']['Associations']['ResourceID']
        except:
            msg = 'Missing Associations->ResourceID (DocType={}, ResourceID={})'.format(doctype, resourceid)
            logg2.error(msg)
            pa.FinishActivity(False, msg)
            return (False, msg)
        
        obj = None
        try:
            obj, created = EntityHistory.objects.get_or_create(DocumentType=doctype, ResourceID=resourceid, ReceivedTime=ts, EntityJSON=jsondata)
            obj.save()
            logg2.info('New GLUE2 EntityHistory.ID={} (DocType={}, ResourceID={})'.format(obj.ID, obj.DocumentType, obj.ResourceID))
        except (ValidationError) as e:
            msg = 'Exception on GLUE2 EntityHistory (DocType={}, ResourceID={}): {}'.format(obj.DocumentType, obj.ResourceID, e.error_list)
            pa.FinishActivity(False, msg)
            return (False, msg)
        except (DataError, IntegrityError) as e:
            msg = 'Exception on GLUE2 EntityHistory (DocType={}, ResourceID={}): {}'.format(obj.DocumentType, obj.ResourceID, e.error_list)
            pa.FinishActivity(False, msg)
            return (False, msg)

        g2doc = Glue2NewMonitoring(doctype, resourceid, ts, 'EntityHistory.ID=%s' % obj.ID)
        try:
            response = g2doc.process(jsondata)
        except (ValidationError, ProcessingException) as e:
            pa.FinishActivity(False, e.response)
            return (False, e.response)
        pa.FinishActivity(True, response)
        return (True, response)

class Glue2DeleteExpiredMonitoring():
    def __init__(self, interval = 3600):
        # Default to doing an expiration check once an hour (3600/seconds)
        self.LastTimestamp = datetime.utcnow()
        self.ExpireInterval = timedelta(seconds=interval)
        self.ExpireCount = 0

    def delete(self):
        if self.LastTimestamp + self.ExpireInterval >= datetime.utcnow():
            return (True, '')
        
        ExpireCountSave = self.ExpireCount
        for t in TestResult.objects.all():
            try:
                validity = timedelta(seconds=int(t.EntityJSON['Validity']))
            except:
                continue
            try:
                creation = t.CreationTime
            except:
                continue
            now = datetime.now(utc)
            if creation + validity < now:
                self.ExpireCount += 1
                logg2.info('Expiring {} + {} < {}: ID={}'.format(creation, validity, now, t.ID))
                t.delete()

        self.LastTimestamp = datetime.utcnow()
        ExpireTotal = self.ExpireCount - ExpireCountSave
        if ExpireTotal > 0:
            return(False, 'Expired {}'.format(ExpireTotal))
        else:
            return(True, '')
