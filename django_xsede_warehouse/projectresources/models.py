from django.db import models
#import jsonfield

# Create your models here.

class ProjectResource(models.Model):
    project_number = models.CharField(db_index=True,max_length=32)
    ResourceID = models.CharField(db_index=True, max_length=40)
    class Meta:
        db_name = 'xcsr'
    def __str__(self):
       return str(self.ResourceID)
