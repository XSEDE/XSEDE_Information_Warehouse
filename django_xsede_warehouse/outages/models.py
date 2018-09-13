from django.db import models
#import jsonfield

# Create your models here.

class Outages(models.Model):
    #Replaced when we found out that the outage pk={outageid + resoureid)
    #id = models.AutoField(primary_key=True, null=False)
    #OutageID,ResourceID,WebURL,Subject,Content,OutageStart,OutageEnd,SiteID
    ID = models.CharField(primary_key=True, max_length=128, null=False)
    OutageID = models.IntegerField(null=False)
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
    def __str__(self):
       return str(self.OutageID)
