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
    "twitter" : {
      "properties" : {
        "content" : {
          "type" :    "string",
          "analyzer": "english"
        }, 
      }
    }
  }
}

# create
if es.indices.exists(index="debug"):
    es.indices.delete(index="debug")
# create is most useful when you want to specify settings and mappings
es.indices.create(index="debug", body=index_config)

# populate and refresh
list_twitter = [
{
    "content" : "pop rock",
}
,
{
    "content" : "pop pop",
}
,
{
    "content" : "rock rock",
}
,
{
    "content" : "rockfeller",
}

]


for ind, e in enumerate(list_twitter):
    es.index(index="debug", doc_type="twitter", id=ind+1, body=e)
es.indices.refresh(index="debug")

q = {
    "query": {
        "filtered": {
            "filter": {
                "bool": {
                    "should": [
                        {
                            "query": {
                                "match": {
                                    "content": "pop"
                                }
                            }
                        },
#                        {
 #                           "match_phrase": {
  #                              "content": {
   #                                 "query": "rock rock"
    #                            }
     #                       }
      #                  }
                    ]
                }
            }
        }
    }
}

pp.pprint(es.search(index="debug", doc_type="twitter", body=q)) 
