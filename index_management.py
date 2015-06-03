# -*- coding: utf-8 -*-
from datetime import datetime
from elasticsearch import Elasticsearch
import pprint

pp = pprint.PrettyPrinter(indent=1)

# by default we connect to localhost:9200
es = Elasticsearch()

# creating index, specifying config, instead of letting system decide on the default via dynamic mapping
# these to specify before indexing any data : 1) settings: number of primary shards/replicas; 2) analyzers, mappings

print 'create index, and specify the mapping at creation time'
gb_mapping = \
{
  "mappings": {
    "tweet" : {
      "properties" : {
        "content" : {
          "type" :    "string",
          "analyzer": "english"
        } 
      }
    }
  }
}
if es.indices.exists(index="gb3"):
    es.indices.delete(index="gb3")
    
es.indices.create(index="gb3", body=gb_mapping)
print 'checking mapping'
pp.pprint(es.indices.get_mapping(index="gb3", doc_type="tweet"))
d = {"content": "pop rock"}
print 'created doc', es.index(index="gb3", doc_type="content", id=1, body=d) 
# refresh is key to make changes available for search
es.indices.refresh(index="gb3")
print es.search(index="gb3", doc_type="content", body={"query": {"match_all":{}}})

print 'delete type'
es.indices.delete_mapping(index="gb3", doc_type="tweet")
