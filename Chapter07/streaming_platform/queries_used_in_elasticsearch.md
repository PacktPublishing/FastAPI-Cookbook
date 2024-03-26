# top ten songs by country
GET songs_index/_search?pretty=true
```json
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": [
        {
          "exists": {
            "field": "views_per_country.Italy"
          }
        }
      ]
    }
  },
  "_source": [
    "title",
    "views_per_country.Italy",
    "album.title",
    "artist"
  ],
  "sort": {
    "views_per_country.Italy": {
      "order": "desc"
    }
  },
  "size": 10
}
```


# top ten artists by country
GET songs_index/_search?pretty=true
```json
{
  "query": {
    "bool": {
      "filter": [
        {
          "exists": {
            "field": "views_per_country.Italy"
          }
        }
      ]
    }
  },
  "size": 0,
  "aggs": {
    "top_artists": {
      "terms": {
        "field": "artist",
        "order": {
          "views": "desc"
        },
        "size": 10
      },
      "aggs": {
        "views": {
          "sum": {
            "field": "views_per_country.Italy",
            "missing": 0
          }
        }
      }
    }
  }
}
```