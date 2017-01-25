from django.db import models
import jsonfield

# Create your models here.

class Outages(models.Model):
    #id = models.AutoField(primary_key=True, null=False)
#OutageID,ResourceID,WebURL,Subject,Content,OutageStart,OutageEnd,SiteID
    OutageID = models.IntegerField(primary_key=True, null=False)
    ResourceID = models.CharField(max_length=64)
    WebURL = models.CharField(max_length=320)
    Subject = models.CharField(db_index=True, max_length=120)
    Content = models.CharField(db_index=True, max_length=1536)
    OutageStart = models.DateTimeField(null=True)
    OutageEnd = models.DateTimeField(null=True)
    SiteID = models.CharField(db_index=True, max_length=40)
    OutageType = models.CharField(max_length=16)
    class Meta:
        db_name = 'xcsr'
    def __unicode__(self):
       return str(self.OutageID)
