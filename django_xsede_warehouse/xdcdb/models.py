from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class TGResource(models.Model):
    ResourceID = models.CharField(primary_key=True,max_length=40)
    #ResourceName = models.CharField(db_index=True, max_length=120)
    SiteID = models.CharField(db_index=True, max_length=40)
    OrganizationAbbrev = models.CharField(db_index=True, max_length=40)
    OrganizationName = models.CharField(db_index=True, max_length=120)
    AmieName = models.CharField(db_index=True, max_length=40)
    PopsName = models.CharField(db_index=True, max_length=120)
    TgcdbResourceName = models.CharField(db_index=True, max_length=40)
    ResourceCode = models.CharField(db_index=True, max_length=40)
    ResourceDescription = models.CharField(db_index=True, max_length=40)
    Timestamp = models.DateTimeField(null=True)
    class Meta:
        db_name = 'xcsr'
    def __str__(self):
       return str(self.ResourceID)

class XSEDELocalUsermap(models.Model):
    ID = models.AutoField(primary_key=True, null=False)
    person_id = models.IntegerField(null=False)
    portal_login = models.CharField(db_index=True, max_length=30, null=False)
    resource_id = models.IntegerField(null=False)
    resource_name = models.CharField(max_length=200, null=False)
    local_username = models.CharField(max_length=30, null=False)
    ResourceID = models.CharField(max_length=40, null=False)
    class Meta:
        unique_together = ['resource_id', 'local_username']
        db_name = 'xcsr'
    def __str__(self):
       return str(self.ID)

class XSEDEPerson(models.Model):
    person_id = models.IntegerField(primary_key=True, null=False)
    portal_login = models.CharField(db_index=True, max_length=30, null=False)
    last_name = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=100, null=False)
    middle_name = models.CharField(max_length=60, null=True)
    is_suspended = models.BooleanField(null=False)
    organization = models.CharField(max_length=300, null=False)
    citizenships = models.CharField(max_length=300, null=True)
    emails = models.CharField(max_length=300, null=True)
    addressesJSON = JSONField()
    class Meta:
        db_name = 'xcsr'
    def __str__(self):
       return str(self.person_id)

class XSEDEFos(models.Model):
    field_of_science_id = models.IntegerField(primary_key=True, null=False)
    parent_field_of_science_id = models.IntegerField(null=True, blank=True)
    field_of_science_desc = models.CharField(max_length=200, null=False)
    fos_nsf_id = models.IntegerField(null=True, blank=True)
    fos_nsf_abbrev = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False)
    class Meta:
        db_name = 'xcsr'
    def __str__(self):
       return str(self.field_of_science_id)
