from __future__ import unicode_literals

from django.db import models

#
# Track processing. Applications should choose an appropriate unique ID
# Avoiding RabbitMQ, GLUE2 or other narrower terminology
#   Topic = what type of information (for example "glue2.applicatios")
#   About = who the information is about (for example "bridges.psc.xsede.org")
#
class ProcessingRecord(models.Model):
    ID = models.CharField(primary_key=True, max_length=255)
    Topic = models.CharField(db_index=True, max_length=255)
    About = models.CharField(db_index=True, max_length=255)
    ProcessingNode = models.CharField(max_length=64)
    ProcessingApp = models.CharField(max_length=64)
    ProcessingStart = models.DateTimeField()
    ProcessingEnd= models.DateTimeField(null=True)
    ProcessingCode = models.CharField(max_length=64, null=True)
    ProcessingMessage = models.CharField(max_length=4096, null=True)
    class Meta:
        db_name = 'xcsr'
    def __unicode__(self):
        return self.ID

#
# A record of processing errors
#
class ProcessingError(models.Model):
    ID = models.AutoField(primary_key=True)
    Exchange = models.CharField(max_length=255)
    RoutingKey = models.CharField(db_index=True, max_length=255)
    ProcessingNode = models.CharField(max_length=64)
    ProcessingApp = models.CharField(db_index=True, max_length=64)
    ErrorTime = models.DateTimeField(db_index=True)
    ErrorCode = models.CharField(max_length=64)
    ErrorMessage = models.CharField(max_length=4096, null=True)
    Reference1 = models.CharField(max_length=255, null=True)
    class Meta:
        db_name = 'xcsr'
    def __unicode__(self):
        return self.ID
