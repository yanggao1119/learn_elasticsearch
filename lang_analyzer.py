# -*- coding: utf-8 -*-
from datetime import datetime
from elasticsearch import Elasticsearch
import pprint

pp = pprint.PrettyPrinter(indent=1)

# by default we connect to localhost:9200
es = Elasticsearch()
es_ind = es.indices
print 'create index, and specify the mapping at creation time'
gb_mapping = \
{
  "mappings": {
    "tweet" : {
      "properties" : {
        "tweet" : {
          "type" :    "string",
        },
        "date" : {
          "type" :   "date"
        },
        "name" : {
          "type" :   "string"
        },
        "user_id" : {
          "type" :   "long"
        },
        "tag" : {
          "type" : "string",
          "index" : "not_analyzed"
        } 
      }
    }
  }
}
try:
    es_ind.create(index="gb3", body=gb_mapping)
except:
    pass

print 'checking mapping'
pp.pprint(es_ind.get_mapping(index="gb3", doc_type="tweet"))

# testing the mapping on tweet and on tag
query = 'I am food is here.'
print 'query:', query
print 'standard:', es_ind.analyze(index="gb3", analyzer="standard", field="tweet", text=query)
print 'english:', es_ind.analyze(index="gb3", analyzer="english", field="tweet", text=query)

