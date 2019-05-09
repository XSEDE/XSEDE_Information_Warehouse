from django.db import models

# Create your models here.

class TGResource(models.Model):
    ResourceID = models.CharField(primary_key=True,max_length=32)
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
        #app_label = 'RDRResource'
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
    ResourceID = models.CharField(max_length=32, null=False)
    class Meta:
        unique_together = ['resource_id', 'local_username']
        db_name = 'xcsr'
    def __str__(self):
       return str(self.ID)
