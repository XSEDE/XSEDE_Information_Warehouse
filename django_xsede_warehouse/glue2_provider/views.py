from django.shortcuts import render
from django.http import *
from django.db import DataError, IntegrityError
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your views here.
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.views import APIView
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from glue2_db.models import EntityHistory
from glue2_provider.process import Glue2NewDocument
from processing_status.process import ProcessingActivity
from xsede_warehouse.exceptions import ProcessingException

import logging
logg2 = logging.getLogger('xsede.glue2')

#import os
import pdb

class Glue2ProcessDoc(APIView):
#    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def post(self, request, doctype, resourceid, format=None):
#       pdb.set_trace()
        receivedts = timezone.now()
        pa_id = '{}:{}'.format(doctype, resourceid)
        pa = ProcessingActivity('glue2_provider.views', 'Glue2ProcessDoc', pa_id, doctype, resourceid)

        if doctype not in ['glue2.applications', 'glue2.compute', 'glue2.computing_activities']:
            logg2.info('Ignoring DocType (DocType=%s, ResourceID=%s)' % \
                       (doctype, resourceid))
            pa.FinishActivity('ignored', 'Ignoring DocType=' + doctype)
            return Response('Ignoring DocType(%s)' % doctype, \
                            status=status.HTTP_400_BAD_REQUEST)
        if 'ID' in request.data and request.data['ID'].startswith('urn:glue2:ComputingActivity:'):
            logg2.debug('Ignoring DocType (DocType=%s, ResourceID=%s) actually glue2.computing_activity' % \
                       (doctype, resourceid))
            pa.FinishActivity('ignored', 'Ignoring DocType=' + doctype)
            return Response('Ignoring DocType(%s) actually glue2.computing_activity' % doctype, \
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            model = EntityHistory(DocumentType=doctype, ResourceID=resourceid, ReceivedTime=receivedts, EntityJSON=request.data)
            model.save()
            logg2.info('New GLUE2 EntityHistory.ID=%s DocType=%s ResourceID=%s' % \
                       (model.ID, model.DocumentType, model.ResourceID))
        except (ValidationError) as e:
            logg2.error('Exception on GLUE2 EntityHistory DocType=%s, ResourceID=%s: %s' % \
                        (model.DocumentType, model.ResourceID, e.error_list))
            pa.FinishActivity('EntityHistory ValidationError', e.error_list)
            return Response('EntityHistory create exception(%s)' % e, \
                            status=status.HTTP_400_BAD_REQUEST)
        except (DataError, IntegrityError) as e:
            logg2.error('Exception on GLUE2 EntityHistory (DocType=%s, ResourceID=%s): %s' % \
                        (model.DocumentType, model.ResourceID, e.error_list))
            pa.FinishActivity('EntityHistory DataError|IntegrityError', e.error_list)
            return Response('EntityHistory create exception(%s)' % e, \
                            status=status.HTTP_400_BAD_REQUEST)
    
        g2doc = Glue2NewDocument(doctype, resourceid, receivedts, 'EntityHistory.ID=%s' % model.ID)
        try:
            response = g2doc.process(request.data)
            pa.FinishActivity('0', 'EntityHistory.ID={}'.format(model.ID))
            return Response(response, status=status.HTTP_201_CREATED)
        except ProcessingException, e:
            pa.FinishActivity('Glue2 ProcessingException', 'status={}; response={}'.format(e.status, e.response))
            return Response(e.response, status=e.status)
