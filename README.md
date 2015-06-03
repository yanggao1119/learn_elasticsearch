### Basics for ElasticSearch
- based on Lucene, yet more comprehensive;
- distributed, every field is indexed and searchable (with Mongo you have to predefine some fields to be indexed, and you can have only one text index);
- scalable to hundreds of servers and petabytes of structured and unstructured data (text);
- RESTful API for lang other than Java;

### Tips

- it takes time for newly indexed data to be available for search. therefore don't panic. Run a refresh command to make the change immediately available;
- array is exactly the same as concatenated strings, as long as search result is concerned;
- idf is not exact: for performance reasons, Elasticsearch doesn’t calculate the IDF across all documents in the index. Instead, each shard calculates a local IDF for the documents contained in that shard. Therefore, for tasks that are not efficiency-critical, such as offline task or debugging/learning code, explicitly set number_of_shards as 1;
- to improve search results:
    - multiple analyzers to balance between precision and recall;
    - query-time boosting
- to shut down all nodes in elasticsearch, seems that sometimes you need to restart computer for it to take effect (at least the case for mac)
    `curl -XPOST 'http://localhost:9200/_shutdown' `
- can delete multiple indexes at once:
    `$ curl -XDELETE 'localhost:9200/us,megacorp,relevance,gb2,muko_track,mukodb,mukodb5?pretty'`
    and check effect by listing all indices:
    `$ curl 'localhost:9200/_cat/indices?v'`
- highlight is very useful for knowing what is going on. For example, we can find that songs with tag "break up" and "grow up" match tag "pump up" just because the sharing of up. Then we can have a more strict sloppy phrase match!
- However, highlight is buggy, it can highlight matches in a field that we are not searching for. But the scoring is not affected, therefore do not panic; 
- Either elastic search or the python client is buggy:
    - under a bool clause, we can put two "must" clauses; yet if one of the must clauses has another bool clause, ES will be confused, and treat the higher-level must as "should"; It only works when there is no embedded bool. Therefore, the way to avoid this bug is to put the two "must" clauses in a list.
    - self-defined analyzer will only be recognizable if specified as argument for "fields"
