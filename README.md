# ElasticSearch Mass Import
A simple way to import all text or csv files from a directory into ES

<center>
  <img src="https://transfer.sh/6nm4fX/Code_1LLf7tmOev.png">
</center>

### How it works
The lazy way
```
PUT request -> http://localhost:9200/_bulk?refresh=true
Data: Your data formatted into JSON
```

### Searching
GET -> `http://localhost:9200/logs/_search?q=testing`
RESP:
```json
{
  "took": 8,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 12,
      "relation": "eq"
    },
    "max_score": 16.936752,
    "hits": [
      {
        "_index": "logs",
        "_type": "_doc",
        "_id": "JxNYuYMBaByoIytW0sGy",
        "_score": 16.936752,
        "_source": {
          "title": "test-data.csv",
          "data": "827274661,79995704248,testtest52,Tests,Testing",
          "date_added": "2022-10-08T20:42:42.978343"
        }
      }
    ]
  }
}
```
