from django.db import models
from rdr_db.models import RDRResource
#import jsonfield
from django.contrib.postgres.fields import JSONField

# The abstract GLUE2 model
class AbstractGlue2Model(models.Model):
    ID = models.CharField(primary_key=True, max_length=200)
    ResourceID = models.CharField(db_index=True, max_length=40)
    Name = models.CharField(max_length=128, null=True)
    CreationTime = models.DateTimeField()
    EntityJSON = JSONField()
    class Meta:
        abstract = True
        db_name = 'glue2'
    def __unicode__(self):
        return self.ID

# The actual GLUE2 models
class ApplicationEnvironment(AbstractGlue2Model):
    Description = models.CharField(max_length=512, null=True)
    AppName = models.CharField(max_length=64)
    AppVersion = models.CharField(max_length=64, default='none')

class ApplicationHandle(AbstractGlue2Model):
    ApplicationEnvironment = models.ForeignKey(ApplicationEnvironment,
                                               related_name='applicationhandles',
                                               null=True)
    Type = models.CharField(max_length=16)
    Value = models.CharField(max_length=64)

class AbstractService(AbstractGlue2Model):
    ServiceType = models.CharField(max_length=32)
    Type = models.CharField(max_length=32)
    QualityLevel = models.CharField(max_length=16, null=True)

class Endpoint(AbstractGlue2Model):
    AbstractService = models.ForeignKey(AbstractService,
                                        related_name='endpoints', null=True)
    HealthState = models.CharField(max_length=16)
    ServingState = models.CharField(max_length=16)
    URL = models.CharField(max_length=320)
    QualityLevel = models.CharField(max_length=16, null=True)
    InterfaceVersion = models.CharField(max_length=16)
    InterfaceName = models.CharField(max_length=32)

class ComputingManager(AbstractGlue2Model):
    pass

class ExecutionEnvironment(AbstractGlue2Model):
    pass

class Location(AbstractGlue2Model):
    pass

class ComputingShare(AbstractGlue2Model):
    pass

class ComputingActivity(AbstractGlue2Model):
    pass

# Where we store every raw document we process
class EntityHistory(models.Model):
    ID = models.AutoField(primary_key=True)
    DocumentType = models.CharField(db_index=True, max_length=32)
    ResourceID = models.CharField(db_index=True, max_length=40)
    ReceivedTime = models.DateTimeField()
    EntityJSON = JSONField()
    class Meta:
        db_name = 'glue2'
