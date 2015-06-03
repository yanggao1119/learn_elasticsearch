from datetime import datetime
from elasticsearch import Elasticsearch
import pprint

pp = pprint.PrettyPrinter(indent=1)

# by default we connect to localhost:9200
es = Elasticsearch()
es_ind = es.indices

list_employee = [
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
,
{
    "first_name" :  "Jane",
    "last_name" :   "Smith",
    "age" :         32,
    "about" :       "I like to collect rock albums",
    "interests":  [ "music" ]
}
,
{
    "first_name" :  "Douglas",
    "last_name" :   "Fir",
    "age" :         35,
    "about":        "I like to build cabinets",
    "interests":  [ "forestry" ]
}
]

for ind, e in enumerate(list_employee):
    es.index(index="megacorp", doc_type="employee", id=ind+1, body=e)

print 'check index'
for ind, e in enumerate(list_employee):
    print es.get(index="megacorp", doc_type="employee", id=ind+1)

# corresponds to "curl -XGET .../_search" at the command line
print 'trying search'
pp.pprint(es.search(index="megacorp", doc_type="employee", body={"query": {"match_all": {}}}) )

print 'search by last_name Smith'
pp.pprint(es.search(index="megacorp", doc_type="employee", body={"query": {"match": {"last_name": "Smith"}}}) )

print 'search by last_name Smith and age > 30'
q={
    "query" : {
        "filtered" : {
            "filter" : {
                "range" : {
                    "age" : { "gt" : 30 } 
                }
            },
            "query" : {
                "match" : {
                    "last_name" : "smith" 
                }
            }
        }
    }
}
pp.pprint(es.search(index="megacorp", doc_type="employee", body=q) )

print 'full-text search'
q={
    "query" : {
        "match" : {
            "about" : "rock climbing"
        }
    }
}
pp.pprint(es.search(index="megacorp", doc_type="employee", body=q) )

# params can be found from the python documentation
print 'not returning source field'
pp.pprint(es.search(index="megacorp", doc_type="employee", body=q, _source=False) )
print 'full-text search, return selected fields from _source, as defined in a list'
pp.pprint(es.search(index="megacorp", doc_type="employee", body=q, _source=["first_name", "about"]) )

print 'try update'
print 'b4'
print es.get(index="megacorp", doc_type="employee", id=1)
d = {"doc": {"last_name": "Zhou", "daughter": "Vivian"}}
es.update(index="megacorp", doc_type="employee", id=1, body=d)
# note that version number also gets incremented
print 'after'
print es.get(index="megacorp", doc_type="employee", id=1)

print 'retrieving multiple docs at one call is good for speed'
# this is most configurable way, each list item can have very different returns
list_docs = \
{
   "docs" : [
      {
         "_index" : "megacorp",
         "_type" :  "employee",
         "_id" :    2
      },
      {
         "_index" : "megacorp",
         "_type" :  "employee",
         "_id" :    1,
         "_source": "last_name"
      }
   ]
}
pp.pprint( es.mget(body=list_docs) )

print 'mget with simplified format'
list_docs = \
{
   "docs" : [
      {
         "_id" :    2
      },
      {
         "_id" :    1,
         "_source": "last_name"
      }
   ]
}
pp.pprint( es.mget(index="megacorp", doc_type="employee", body=list_docs) )

# mapping is defined on the doc_type level
print "get mapping for all fields, for analysis"
pp.pprint(es_ind.get_mapping(index="megacorp", doc_type="employee"))

# default analyzer is the standard analyzer
print 'testing analyzers'
print es_ind.analyze(index="megacorp", analyzer="standard", text="text to analyse!")

print 'create index, and specify the mapping at creation time'
gb_mapping = \
{
  "mappings": {
    "tweet" : {
      "properties" : {
        "tweet" : {
          "type" :    "string",
          "analyzer": "english"
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
query = 'Black-cats'
print 'query:', query
print 'twitter:', es_ind.analyze(index="gb3", analyzer="standard", field="tweet", text=query)
print 'tag', es_ind.analyze(index="gb3", analyzer="standard", field="tag", text=query)
