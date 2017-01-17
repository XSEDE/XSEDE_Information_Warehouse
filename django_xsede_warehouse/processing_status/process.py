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
    def __init__(self, App, ID, Topic, About):
        self.App = App
        self.ID = ID
        model = ProcessingRecord(ID=ID,
                                Topic=Topic,
                                About=About,
                                ProcessingNode=socket.gethostname(),
                                ProcessingApp=self.App,
                                ProcessingStart=datetime.now(utc)
                                 )
        model.save()
        self.model = model

    def FinishActivity(self, Code, Message):
        self.model.ProcessingEnd=datetime.now(utc)
        self.model.ProcessingCode=Code
        self.model.ProcessingMessage=Message
        self.model.save()