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

            logg2.info('ID=%s, ResourceID=%s, Name="%s"' % (self.new[me][ID]['ID'], self.resourceid, self.new[me][ID]['Name']))

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
