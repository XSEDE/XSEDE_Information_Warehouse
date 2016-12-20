from __future__ import print_function
import json
from datetime import datetime, tzinfo
from django.utils import timezone
from django.db import DataError, IntegrityError
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from monitoring_db.models import *
from glue2_db.models import *

from rest_framework import status
from xsede_warehouse.exceptions import ProcessingException

import pdb
import logging
logg2 = logging.getLogger('xsede.glue2')

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
        self.newAbsServType = {}

    def LoadNewMonitoringService(self, model, obj):
        if type(obj) is not dict:
            raise ValidationError('New entity %s doesn\'t contain a dictionary' % model)

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
                    isservice= True
            except KeyError:
                isservice = False

            try:
                if extension['ErrorMessage']:
                    errormessage = extension['ErrorMessage']
            except KeyError:
                errormessage = None

            print('ID=%s, ResourceID=%s, Name="%s"' % (self.new[me][ID]['ID'], self.resourceid, self.new[me][ID]['Name']))

            try:
                nagios_m, created = TestResult.objects.get_or_create(ID=self.new[me][ID]['ID'],
                                                                 defaults={"ResourceID": self.resourceid,
                                                                           "Name": self.new[me][ID]['Name'],
                                                                           "CreationTime": self.new[me][ID]['CreationTime'],
                                                                             "EntityJSON": self.new[me][ID],
                                                                             "Source": extension['Source'].lower(),
                                                                             "Result": extension['Result'].lower(),
                                                                             "ErrorMessage": errormessage,
                                                                             "IsSoftware" : issoftware,
                                                                             "IsService": isservice})
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
                raise ProcessingException('%s updating %s (ID=%s): %s' % (type(e).__name__, me, self.new[me][ID]['ID'], e.message), \
                                          status=status.HTTP_400_BAD_REQUEST)

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
            raise ValidationError(msg)
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

    """
    def process_1(self, data):
        start = datetime.utcnow()
        m = 'TestResult'

        if self.doctype == 'inca':
            if 'rep:report' not in data\
                or 'XSEDE_IS' not in data\
                or any(x not in data['rep:report'] for x in ('gmt', 'name', 'hostname')):
                print ('Inca JSON response is missing a \'rep:report\' element')
            else:
                source = 'inca'
                report = data['rep:report']
                resource_info = data['XSEDE_IS']
                result = report['exitStatus']
                status = result['completed']
                if status:
                    status = 'success'
                else:
                    status = 'failure'
                try:
                    errormessage = result['errorMessage']
                except KeyError:
                    errormessage = None
                print ('ID=%s, ResourceID=%s, Name="%s"' % (resource_info['ID'], self.resourceid, resource_info['Name']))

                try:
                    inca_m, created = TestResult.objects.get_or_create(ID=resource_info['ID'],
                                                                   defaults={"ResourceID": self.resourceid,
                                                                             "Name": resource_info['Name'],
                                                                             "CreationTime": report['gmt'],
                                                                             "EntityJSON": report,
                                                                             "Source": source,
                                                                             "Result": status,
                                                                             "ErrorMessage": errormessage})
                    if not created:
                        if parse_datetime(report['gmt']) > inca_m.CreationTime:
                            TestResult.objects.filter(ID=resource_info['ID']).update(ResourceID=self.resourceid,
                                                                             Name=resource_info['Name'],
                                                                             CreationTime=report['gmt'],
                                                                             EntityJSON=report,
                                                                             Source=source,
                                                                             Result=status,
                                                                             ErrorMessage=errormessage)
                except (DataError, IntegrityError) as e:
                    logg2.error('Exception updating %s (ID=%s): %s' % (m, self.resourceid, e.message))

        elif self.doctype == 'nagios':
                extension = data['Extension']
                associations = data['Associations']
                issoftware = False
                isservice = False
                errormessager = None

                try:
                    if associations['SoftwareID']:
                        issoftware = True
                except KeyError:
                    issoftware = False
                try:
                    if associations['ServiceID']:
                        isservice= True
                except KeyError:
                    isservice = False
                try:
                    if extension['ErrorMessage']:
                        errormessage = extension['ErrorMessage']
                except KeyError:
                    errormessage = None

                print ('ID=%s, ResourceID=%s, Name="%s"' % (data['ID'], self.resourceid, data['Name']))

                try:
                    nagios_m, created = TestResult.objects.get_or_create(ID=data['ID'],
                                                                   defaults={"ResourceID": self.resourceid,
                                                                             "Name": data['Name'],
                                                                             "CreationTime": data['CreationTime'],
                                                                             "EntityJSON": data,
                                                                             "Source": extension['Source'].lower(),
                                                                             "Result": extension['Result'].lower(),
                                                                             "ErrorMessage": errormessage,
                                                                             "IsSoftware" : issoftware,
                                                                             "IsService": isservice})
                    if not created:
                        if parse_datetime(data['CreationTime']) > nagios_m.CreationTime:
                            TestResult.objects.filter(ID=data['ID']).update(ResourceID=self.resourceid,
                                                                             Name=data['Name'],
                                                                             CreationTime=data['CreationTime'],
                                                                             EntityJSON=data,
                                                                             Source=extension['Source'].lower(),
                                                                             Result=extension['Result'].lower(),
                                                                             ErrorMessage=errormessage,
                                                                             IsSoftware=issoftware,
                                                                             IsService=isservice)
                except (DataError, IntegrityError) as e:
                    logg2.error('Exception updating %s (ID=%s): %s' % (m, self.resourceid, e.message))


        end = datetime.utcnow()
        self.stats['ProcessingSeconds'] = (end - start).total_seconds()
        logg2.info(StatsSummary(self.stats))
        return(self.stats)
    """

class Glue2Process():
    def process(self, doctype, resourceid, data):
        if doctype not in ['glue2.applications', 'glue2.compute', 'glue2.computing_activities','inca','nagios']:
            logg2.info('Ignoring DocType (DocType=%s, ResourceID=%s)' % \
                       (doctype, resourceid))
            return 'Ignoring DocType(%s)' % doctype

        model = None
        receivedts = timezone.now()
        try:
            # data = json.loads(data)
            model = EntityHistory(DocumentType=doctype, ResourceID=resourceid, ReceivedTime=receivedts, EntityJSON=data)
            model.save()
            logg2.info('New GLUE2 EntityHistory.ID=%s DocType=%s ResourceID=%s' % \
                       (model.ID, model.DocumentType, model.ResourceID))
        except (ValidationError) as e:
            logg2.error('Exception on GLUE2 EntityHistory DocType=%s, ResourceID=%s: %s' % \
                        (model.DocumentType, model.ResourceID, e.error_list))
            return 'EntityHistory create exception(%s)' % e
        except (DataError, IntegrityError) as e:
            logg2.error('Exception on GLUE2 EntityHistory (DocType=%s, ResourceID=%s): %s' % \
                        (model.DocumentType, model.ResourceID, e.error_list))
            return 'EntityHistory create exception(%s)' % e

        g2doc = Glue2NewDocument(doctype, resourceid, receivedts, 'EntityHistory.ID=%s' % model.ID)
        try:
            response = g2doc.process(data)
            return response
        except ProcessingException as e:
            return e.response