from __future__ import unicode_literals

from django.db import models
from glue2_db.models import AbstractGlue2Model
import jsonfield

# The actual GLUE2 models
class TestResult(AbstractGlue2Model):
    ResourceID = models.CharField(db_index=True, max_length=40)
    Source = models.CharField(max_length=16)
    Result = models.CharField(max_length=16)
    ErrorMessage = models.CharField(max_length=4096, null=True)
    IsSoftware = models.BooleanField(default=False)
    IsService = models.BooleanField(default=False)
