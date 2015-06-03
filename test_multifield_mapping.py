from datetime import datetime
from elasticsearch import Elasticsearch
import pprint

pp = pprint.PrettyPrinter(indent=1)

# by default we connect to localhost:9200
es = Elasticsearch()

# index config
# default number_of_shards=5, which cannot be changed after index creation;
# yet idf is computed within each shard, for efficiency reasons; 
# if it is not efficiency-critical task, such as offline task or learning code
# explicitly set number_of_shards as 1
index_config = \
{
  "settings": {
    "number_of_shards": 1
  }
  ,
  "mappings": {
    "track" : {
      "properties" : {
        "tag_str" : {
          "type" :    "string",
          "analyzer": "english",
          "fields" : {
            "exact" : {
              "type" : "string",
              "index":  "not_analyzed"
            }
          }
        } 
      }
    }
  }
}

# create
if es.indices.exists(index="test"):
    es.indices.delete(index="test")
# create is most useful when you want to specify settings and mappings
es.indices.create(index="test", body=index_config)

# populate and refresh
list_track = [
{
    "tag_str" : "pop rocks",
}
,
{
    "tag_str" : "pop rock",
}
]

for ind, e in enumerate(list_track):
    es.index(index="test", doc_type="track", id=ind+1, body=e)
es.indices.refresh(index="test")

# print data
print 'print data'
for ind, e in enumerate(list_track):
    pp.pprint(es.get(index="test", doc_type="track", id=ind+1))

# seems that array is exactly the same as concat string
print 'search tag_str'
# simple query using one field
#q = {
 #   "query" : {
  #      "match" : {
   #         "tag_str" : "pop rocks"
    #    }
#    }
#}

# multi_match query using multiple fields
# TODO: can we just use exact match??
q = {
    "query" : {
        "multi_match" : {
            "query" : "pop rocks",
            "type" : "most_fields",
            #"fields": ["tag_str"]
            "fields": ["tag_str.exact^10"]
            #"fields": ["tag_str", "tag_str.exact^10"]
        }
    }
}

pp.pprint(es.search(index="test", doc_type="track", body=q) )
