curl -XPUT 'localhost:9200/megacorp/employee/1' -d '
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
'

curl -XPUT 'localhost:9200/megacorp/employee/2' -d '
{
    "first_name" :  "Jane",
    "last_name" :   "Smith",
    "age" :         32,
    "about" :       "I like to collect rock albums",
    "interests":  [ "music" ]
}
'

curl -XPUT 'localhost:9200/megacorp/employee/3' -d '
{
    "first_name" :  "Douglas",
    "last_name" :   "Fir",
    "age" :         35,
    "about":        "I like to build cabinets",
    "interests":  [ "forestry" ]
}
'

# yang inserted to the tutorial
curl -XPUT 'localhost:9200/megacorp/employee/4' -d '
{
    "first_name" :  "Cleopatra",
    "last_name" :   "Gao",
    "age" :         29,
    "about" :       "I like chris martin",
    "interests":  [ "music", "music"]
}
'

# yang inserted to the tutorial
curl -XPUT 'localhost:9200/megacorp/employee/5' -d '
{
    "first_name" : "John2",
    "last_name" :  "Smith-Jones",
    "age" :        35,
    "about" :      "climbing good rock",
    "interests": [ "sports", "music" ]
}
'

curl -XGET localhost:9200/megacorp/employee/_search -d ' 
{
    "query": {
        "match": {
            "last_name": "Smith"
        }
    }
}
'

echo
echo 'smith, age>30'
echo
# filter for hard constraints;
# query for full-text search which is soft constraint, i.e., last name contains something like Smith
curl -XGET localhost:9200/megacorp/employee/_search -d ' 
{
    "query": {
        "filtered": {
            "filter": {
                "range": {
                    "age": {"gt": 30}
                }
            },
            "query": {
                "match": {
                    "last_name": "Smith"
                }
            }
        } 
    }
}
'

echo
echo "full text, rock climbing"
echo

curl -XGET localhost:9200/megacorp/employee/_search -d ' 
{
    "query": {
                "match": {
                    "about": "rock climbing"
                }
    }
}
'

# a list is the same as a string concatenated
echo
echo "full text, music"
echo

curl -XGET localhost:9200/megacorp/employee/_search -d ' 
{
    "query": {
                "match": {
                    "interests": "music"
                }
    }
}
'

# a list is similar to a string concatenated
echo
echo "word search"
echo

curl -XGET localhost:9200/megacorp/employee/_search -d ' 
{
    "query": {
                "match": {
                    "about": "rock climbing"
                }
    }
}
'

echo
echo "phrase match"
echo

curl -XGET localhost:9200/megacorp/employee/_search -d ' 
{
    "query": {
        "match_phrase": {
            "about": "rock climbing"
        }
    },
    "highlight": {
        "fields": {
            "about": {}
        }
    }
}
'

#TODO: can this highlighting be used for locating matched substring for NER, even if this match is fuzzy??
# span is returned, matched words are highlighted
echo "highlighting fuzzy match"
curl -XGET localhost:9200/megacorp/employee/_search -d ' 
{
    "query": {
        "match": {
            "about": "rock climbing"
        }
    },
    "highlight": {
        "fields": {
            "about": {}
        }
    }
}
'
