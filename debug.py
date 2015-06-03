from elasticsearch import Elasticsearch
import pprint

pp = pprint.PrettyPrinter(indent=1)

es = Elasticsearch()
if es.indices.exists(index="debug"):
    es.indices.delete(index="debug")

# populate and refresh
list_twitter = [
{
    "content" : "pop rock",
}
,
{
    "content" : "rock rock",
}
,
{
    "content" : "rock",
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
                        {
                            "query": {
                                "match_phrase": { 
                                    "content": "rock-rocks",# a rock",
                                },
                            },

                        }

                    ]
                }
            }
        }
    }
}

pp.pprint(es.search(index="debug", doc_type="twitter", body=q)) 
