from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.

class RDRResource(models.Model):
    rdr_resource_id = models.IntegerField(primary_key=True)
    rdr_type = models.CharField(max_length=16)
    info_resourceid = models.CharField(db_index=True, max_length=40)
    info_siteid = models.CharField(db_index=True, max_length=40)
    resource_descriptive_name = models.CharField(max_length=120)
    resource_description = models.CharField(max_length=4000, null=True)
    resource_status = JSONField()
    current_statuses = models.CharField(max_length=64)
    latest_status = models.CharField(max_length=32, null=True)
    latest_status_begin = models.DateField(null=True)
    latest_status_end = models.DateField(null=True)
    parent_resource = models.IntegerField(db_index=True, null=True)
    recommended_use = models.CharField(max_length=4000, null=True)
    access_description = models.CharField(max_length=4000, null=True)
    project_affiliation = models.CharField(max_length=16, null=True)
    provider_level = models.CharField(max_length=16, null=True)
    other_attributes = JSONField()
    updated_at = models.DateTimeField(null=True)
    class Meta:
        db_name = 'xcsr'
    def __str__(self):
       return str(self.rdr_resource_id)
# Under consideration
#    parent_resource = models.ForeignKey("self", db_constraint=False, null=True)
