from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(hosts=['localhost:9200'], timeout=20)

def bulk_indexing():
    es = Elasticsearch()
    ResourceV3Index.init()
    bulk(client=es, actions=(b.indexing() for b in models.ResourceV3.objects.all().iterator()))
