from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

################################################################################
# This model borrows GLUE2 concepts for global identifiers
################################################################################
class ResourceV2(models.Model):
    # AbstraceGlue2Entity attributes
    ID = models.CharField(primary_key=True, max_length=200)
    Name = models.CharField(max_length=255, null=True)
    CreationTime = models.DateTimeField()
    Validity = models.DurationField(null=True)
    EntityJSON = JSONField()
    # Global Resource attributes
    Affiliation = models.CharField(db_index=True, max_length=32)
    ProviderID = models.CharField(max_length=200, null=True)
    ResourceGroup = models.CharField(max_length=64, null=True)
    Type = models.CharField(max_length=32)
    ShortDescription = models.CharField(max_length=500, null=True)
    Description = models.CharField(max_length=24000, null=True)
    QualityLevel = models.CharField(max_length=16, null=True)
    LocalID = models.CharField(db_index=True, max_length=200, null=True)
    Topics = models.CharField(max_length=1000, null=True)
    Keywords = models.CharField(max_length=1000, null=True)
    Associations = models.CharField(max_length=1000, null=True)
    class Meta:
        db_name = 'glue2'
    def __str__(self):
        return str(self.ID)

class ResourceV2Provider(models.Model):
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
    def __str__(self):
        return str(self.ID)

class ResourceV2Guide(models.Model):
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
    def __str__(self):
        return str(self.ID)

class ResourceV2GuideResource(models.Model):
    # AbstraceGlue2Entity attributes
    ID = models.CharField(primary_key=True, max_length=200)
#    Name = models.CharField(max_length=255, null=True)
#    CreationTime = models.DateTimeField()
#    Validity = models.DurationField(null=True)
#    EntityJSON = JSONField()
    # Global Resource attributes
    CuratedGuideID = models.ForeignKey('ResourceV2Guide', on_delete=models.CASCADE)
    ResourceID = models.ForeignKey('ResourceV2', on_delete=models.CASCADE)
    class Meta:
        db_name = 'glue2'
    def __str__(self):
        return str(self.ID)
