from django.db import models
#import jsonfield

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
    def __unicode__(self):
       return str(self.ResourceID)
