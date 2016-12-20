from django.db import models
import jsonfield

# Create your models here.

class ProjectResource(models.Model):
    project_number = models.CharField(db_index=True,max_length=32)
    ResourceID = models.CharField(db_index=True, max_length=40)
    class Meta:
        #app_label = 'RDRResource'
        db_name = 'xcsr'
    def __unicode__(self):
       return str(self.ResourceID)
