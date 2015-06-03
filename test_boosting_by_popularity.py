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
          "norms": { "enabled": False }
        } 
      }
    }
  }
}

# create
if es.indices.exists(index="relevance"):
    es.indices.delete(index="relevance")
# create is most useful when you want to specify settings and mappings
es.indices.create(index="relevance", body=index_config)

# populate and refresh
list_track = [
{
    "tag_str" : "pop",
    "tag_count": 100
}
,
{
    "tag_str" : "pop pop",
    "tag_count": 1
}
]
for ind, e in enumerate(list_track):
    es.index(index="relevance", doc_type="track", id=ind+1, body=e)
es.indices.refresh(index="relevance")

# print data
print 'print data'
for ind, e in enumerate(list_track):
    pp.pprint(es.get(index="relevance", doc_type="track", id=ind+1))

print 'search tag_str'
# test both the case of single-term and multi-term query
# old
#q = {
 #   "query": { 
  #      "match": { 
   #         "tag_str": "pop"
    #    }
#    }
#}
q = {
    "query": { 
        "function_score": {
            "query": {
                "match": { 
                    "tag_str": "pop"
                }
            },
            "field_value_factor": {
                "field": "tag_count"
            }
        }
    }
}


pp.pprint(es.search(index="relevance", doc_type="track", body=q, explain=True) )
