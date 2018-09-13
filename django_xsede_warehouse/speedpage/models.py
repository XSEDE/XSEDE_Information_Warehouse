from django.db import models
#import jsonfield

# Create your models here.

class speedpage(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    #tstamp = models.DateTimeField(null=True)
    tstamp = models.IntegerField(null=True)
    sourceid = models.CharField(max_length=32)
    source = models.CharField(db_index=True, max_length=120)
    src_url = models.CharField(max_length=320)
    destid = models.CharField(db_index=True, max_length=40)
    dest = models.CharField(db_index=True, max_length=40)
    dest_url = models.CharField(max_length=320)
    xfer_rate = models.CharField(max_length=32)
    class Meta:
        #app_label = 'RDRResource'
        db_name = 'xcsr'
    def __str__(self):
       return str(self.sourceid)
