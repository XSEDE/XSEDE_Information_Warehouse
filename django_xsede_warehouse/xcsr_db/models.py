from django.db import models

# Create your models here.

class ComponentSPRequirement(models.Model):
    SPClass_CHOICES = (('XSEDE Level 1', 'XSEDE Level 1'),
                       ('XSEDE Level 2', 'XSEDE Level 2'),
                       ('XSEDE Level 3', 'XSEDE Level 3'),
                   )
    Requirement_CHOICES = (('Required', 'Required'),
                           ('Optional', 'Optional') )
    
    ComponentName = models.CharField(max_length=64)
    SPClass = models.CharField(max_length=16, choices=SPClass_CHOICES)
    Requirement = models.CharField(max_length=12, choices=Requirement_CHOICES)
    UpdateTime = models.DateTimeField(auto_now=True)
    UpdateUser = models.CharField(max_length=16)
    
    def __unicode__(self):
        return '%s.%s' % (self.ComponentName, self.SPClass)

    class Meta:
        db_name = 'xcsr'
        unique_together = ('ComponentName', 'SPClass')
