from django.db import models
from django.contrib.postgres.fields import JSONField

from elasticsearch_dsl import Document, Text, Keyword, Date

################################################################################
# GLUE2 identifiers (AbstraceGlue2Entity)
#   ID: Unique URI ID across all models and resource types
#   Name: Short descriptive name
#   CreationTime: When the resource was created or refreshed in this catalog
#   Validity: How long after CreationTime to expire the resource
# Global attributes
#   Affiliation: Short descriptive publishing organization name (domain like)
################################################################################
#
# Catalogs that resource information come from
#
class ResourceV3Catalog(models.Model):
    # Record management fields
    ID = models.CharField(primary_key=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Content fields
    Name = models.CharField(max_length=255, null=False, blank=False)
    Affiliation = models.CharField(max_length=32, null=False)
    ShortDescription = models.CharField(max_length=1000, null=False, blank=False)
    # The catalog API metadata access URL (self reference URL)
    CatalogMetaURL = models.URLField(max_length=200, blank=True)
    # The catalog local user interface URL
    CatalogUserURL = models.URLField(max_length=200, blank=True)
    # The catalog API for software (not URLField so we can do sql:<etc> and other URIs)
    CatalogAPIURL = models.CharField(max_length=200, blank=True)
    # The schema for the catalog API for software
    CatalogSchemaURL = models.URLField(max_length=200, blank=True)
    class Meta:
        db_name = 'glue2'
    def __str__(self):
        return str(self.ID)

#
# Local Resource Record (unmodified in EntityJSON)
#
class ResourceV3Local(models.Model):
    # Record management fields
    ID = models.CharField(primary_key=True, max_length=200)
    CreationTime = models.DateTimeField()
    Validity = models.DurationField(null=True)
    Affiliation = models.CharField(db_index=True, max_length=32)
    LocalID = models.CharField(db_index=True, max_length=200, null=True)
    LocalType = models.CharField(max_length=32, null=True)
    LocalURL = models.CharField(max_length=200, null=True)
    # The catalog API metadata access URL (from the ResourceV3Catalog record)
    CatalogMetaURL = models.CharField(max_length=200, null=True)
    # Local unmodified record, should conform to CatalogMetaURL -> CatalogSchemaURL
    EntityJSON = JSONField()
    class Meta:
        db_name = 'glue2'
    def __str__(self):
        return str(self.ID)

#
# Standard Resource Record used for discovery
#
class AbstractResourceV3Model(models.Model):
    # Record management fields
    # Identical to the corresponding ResourceV3Local->ID
    ID = models.CharField(primary_key=True, max_length=200)
    Affiliation = models.CharField(max_length=32)
    LocalID = models.CharField(max_length=200, null=True)
    QualityLevel = models.CharField(max_length=16, null=True)
    # Base content fields
    Name = models.CharField(max_length=255)
    ResourceGroup = models.CharField(max_length=64)
    Type = models.CharField(max_length=64)
    ShortDescription = models.CharField(max_length=1200, null=True)
    ProviderID = models.CharField(max_length=200, null=True)
    Description = models.CharField(max_length=24000, null=True)
    Topics = models.CharField(max_length=1000, null=True)
    Keywords = models.CharField(max_length=1000, null=True)
    Audience = models.CharField(max_length=200, null=True)
    # Event content fields
    StartDateTime = models.DateTimeField(null=True)
    EndDateTime = models.DateTimeField(null=True)

    class Meta:
        abstract = True
        db_name = 'glue2'
    def __str__(self):
        return str(self.ID)
        
class ResourceV3(AbstractResourceV3Model):
    def indexing(self):
        obj = ResourceV3Index(
                meta={'id': self.ID},
                ID = self.ID,
                Affiliation = self.Affiliation,
                LocalID = self.LocalID,
                QualityLevel = self.QualityLevel,
                Name = self.Name,
                ResourceGroup = self.ResourceGroup,
                Type = self.Type,
                ShortDescription = self.ShortDescription,
                ProviderID = self.ProviderID,
                Description = self.Description,
                Topics = self.Topics,
                Keywords = self.Keywords,
                Audience = self.Audience,
                StartDateTime = self.StartDateTime,
                EndDateTime = self.EndDateTime
            )
        obj.save()
        return obj.to_dict(include_meta = True)
#    def delete(self):
#        obj = ResourceV3Index.get(self.ID).delete()
#        return

class ResourceV3Index(Document):
    ID = Keyword()
    Affiliation = Keyword()
    LocalID = Keyword()
    QualityLevel = Keyword()
    Name = Text(fields={'Keyword': Keyword()})
    ResourceGroup = Keyword()
    Type = Keyword()
    ShortDescription = Text()
    ProviderID = Keyword()
    Descripton = Text()
    Topics = Keyword()
    Keywords = Keyword()
    Audience = Keyword()
    StartDateTime = Date()
    EndDateTime = Date()
    class Index:
        name = 'resourcev3-index'

#
#  Resource Relationships
#
class ResourceV3Relation(models.Model):
    ID = models.CharField(primary_key=True, max_length=200)
    FirstResourceID = models.CharField(db_index=True, max_length=200)
    SecondResourceID = models.CharField(db_index=True, max_length=200)
    RelationType = models.CharField(max_length=32, null=False)
    class Meta:
        db_name = 'glue2'
    def __str__(self):
        return str(self.ID)