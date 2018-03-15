from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

################################################################################
# This model borrows GLUE2 concepts for global identifiers
################################################################################
class Resource(models.Model):
    # AbstraceGlue2Entity attributes
    ID = models.CharField(primary_key=True, max_length=200)
    Name = models.CharField(max_length=255, null=True)
    CreationTime = models.DateTimeField()
    Validity = models.DurationField(null=True)
    EntityJSON = JSONField()
    # Global Resource attributes
    Affiliation = models.CharField(db_index=True, max_length=32)
    ProviderID = models.CharField(max_length=200, null=True)
    Type = models.CharField(max_length=32)
    Description = models.CharField(max_length=8000, null=True)
    QualityLevel = models.CharField(max_length=16, null=True)
    LocalID = models.CharField(db_index=True, max_length=32, null=True)
    Keywords = models.CharField(max_length=1000, null=True)
    Associations = models.CharField(max_length=1000, null=True)
    class Meta:
        db_name = 'glue2'
    def __unicode__(self):
        return self.ID

class ResourceProvider(models.Model):
    # AbstraceGlue2Entity attributes
    ID = models.CharField(primary_key=True, max_length=200)
    Name = models.CharField(max_length=255, null=True)
    CreationTime = models.DateTimeField()
    Validity = models.DurationField(null=True)
    EntityJSON = JSONField()
    # Global Resource attributes
    Affiliation = models.CharField(db_index=True, max_length=32)
    LocalID = models.CharField(db_index=True, max_length=32, null=True)
    class Meta:
        db_name = 'glue2'
    def __unicode__(self):
        return self.ID
