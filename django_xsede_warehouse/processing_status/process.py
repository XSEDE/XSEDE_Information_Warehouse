from datetime import datetime, timedelta, tzinfo
from django.utils import timezone

from processing_status.models import *

import json
import logging
import hashlib
import socket
logg2 = logging.getLogger('xsede.logger')

class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return 'UTC'
    def dst(self, dt):
        return timedelta(0)
utc = UTC()

class ProcessingActivity():
    '''
        Application: application name, such as os.path.basename(__file__)
        Function: application function, or 'main' if their is none
        ID: unique ID (pk) for this entry, this value should stay the same between processing
        Topic: type of information, such as 'Outages', 'inca', etc.
        About: which qualified resource (ResourceID) or domain the information is about
    '''
    def __init__(self, Application, Function, ID, Topic, About):
        self.Application = Application
        self.Function = Function
        self.ID = ID
        model = ProcessingRecord(ID=ID,
                                Topic=Topic,
                                About=About,
                                ProcessingNode=socket.gethostname(),
                                ProcessingApplication=self.Application,
                                ProcessingFunction=self.Function,
                                ProcessingStart=datetime.now(utc)
                                 )
        model.save()
        self.model = model

    def FinishActivity(self, Code, Message):
        self.model.ProcessingEnd=datetime.now(utc)
        if Code is False:
            self.model.ProcessingCode='1'
        elif Code is True:
            self.model.ProcessingCode='0'
        else:
            self.model.ProcessingCode=str(Code)
        if isinstance(Message, dict):
            self.model.ProcessingMessage=json.dumps(Message)
        else:
            self.model.ProcessingMessage=Message
        self.model.save()

        if self.model.ProcessingCode != '0':
            errmodel = ProcessingError(Topic=self.model.Topic,
                                     About=self.model.About,
                                     ProcessingNode=self.model.ProcessingNode,
                                     ProcessingApplication=self.model.ProcessingApplication,
                                     ProcessingFunction=self.model.ProcessingFunction,
                                     ErrorTime=self.model.ProcessingEnd,
                                     ErrorCode=self.model.ProcessingCode,
                                     ErrorMessage=self.model.ProcessingMessage,
                                     Reference1=self.model.ID
                                 )
            errmodel.save()
            self.errmodel = errmodel
