from django.db import models
from rdr_db.models import RDRResource
from django.contrib.postgres.fields import JSONField

# The abstract GLUE2 model
class AbstractGlue2Model(models.Model):
    ID = models.CharField(primary_key=True, max_length=200)
    Name = models.CharField(max_length=128, null=True)
    CreationTime = models.DateTimeField()
    Validity = models.DurationField(null=True)
    EntityJSON = JSONField()
    class Meta:
        abstract = True
        db_name = 'glue2'
    def __unicode__(self):
        return self.ID

# GLUE2 models NOT about specific resources
class AdminDomain(AbstractGlue2Model):
    Description = models.CharField(max_length=128, null=True)
    WWW = models.URLField(max_length=200, null=True)
    Distributed = models.NullBooleanField
    Owner = models.CharField(max_length=128, null=True)

class UserDomain(AbstractGlue2Model):
    Description = models.CharField(max_length=128, null=True)
    WWW = models.URLField(max_length=200, null=True)
    Level = models.PositiveIntegerField(null=True)
    UserManager = models.URLField(max_length=200, null=True)
    Member = models.CharField(max_length=128, null=True)

class AccessPolicy(AbstractGlue2Model):
    Scheme = models.CharField(max_length=16, null=True)
    Rule = models.CharField(max_length=128, null=True)

class Contact(AbstractGlue2Model):
    Detail = models.CharField(max_length=128)
    Type = models.CharField(max_length=16)

class Location(AbstractGlue2Model):
    Address = models.CharField(max_length=64, null=True)
    Place = models.CharField(max_length=64, null=True)
    Country = models.CharField(max_length=64, null=True)
    PostCode = models.CharField(max_length=64, null=True)
    Latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

# GLUE 2 models about specific resources
class ApplicationEnvironment(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)
    Description = models.CharField(max_length=512, null=True)
    AppName = models.CharField(max_length=64)
    AppVersion = models.CharField(max_length=64, default='none')

class ApplicationHandle(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)
    ApplicationEnvironment = models.ForeignKey(ApplicationEnvironment,
                                               related_name='applicationhandles',
                                               null=True)
    Type = models.CharField(max_length=16)
    Value = models.CharField(max_length=64)

class AbstractService(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)
    ServiceType = models.CharField(max_length=32)
    Type = models.CharField(max_length=32)
    QualityLevel = models.CharField(max_length=16, null=True)

class Endpoint(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)
    AbstractService = models.ForeignKey(AbstractService,
                                        related_name='endpoints', null=True)
    HealthState = models.CharField(max_length=16)
    ServingState = models.CharField(max_length=16)
    URL = models.CharField(max_length=320)
    QualityLevel = models.CharField(max_length=16, null=True)
    InterfaceVersion = models.CharField(max_length=16)
    InterfaceName = models.CharField(max_length=32)

class ComputingManager(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)

class ExecutionEnvironment(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)

class ComputingShare(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)

class ComputingActivity(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)

# Where we store every raw document we process
class EntityHistory(models.Model):
    ID = models.AutoField(primary_key=True)
    DocumentType = models.CharField(db_index=True, max_length=32)
    ResourceID = models.CharField(db_index=True, max_length=40)
    ReceivedTime = models.DateTimeField()
    EntityJSON = JSONField()
    class Meta:
        db_name = 'glue2'
