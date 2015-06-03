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
          #"analyzer": "english"
          "index" : "not_analyzed"
        } 
      }
    }
  }
}

# create
if es.indices.exists(index="toy"):
    es.indices.delete(index="toy")
# create is most useful when you want to specify settings and mappings
es.indices.create(index="toy", body=index_config)

# populate and refresh
list_track = [
{
    "tag_str" : "pop"
}
,
{
    "tag_str" : "rock pop"
}
,
{
    "tag_str" : "rock pop pop"
}

]
for ind, e in enumerate(list_track):
    es.index(index="toy", doc_type="track", id=ind+1, body=e)
es.indices.refresh(index="toy")

# print data
print 'print data'
for ind, e in enumerate(list_track):
    pp.pprint(es.get(index="toy", doc_type="track", id=ind+1))

print 'search tag_str'
# test both the case of single-term and multi-term query
pp.pprint(es.search(index="toy", doc_type="track", body={"query": {"prefix": {"tag_str": "pop"}}}) )
