from datetime import datetime, timedelta, tzinfo
from django.utils import timezone

from processing_status.models import *

import logging
import hashlib
import socket
logg2 = logging.getLogger('xsede.glue2')

class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return 'UTC'
    def dst(self, dt):
        return timedelta(0)
utc = UTC()

class ProcessingActivity():
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
        self.model.ProcessingCode=Code
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
