#multipul conditions match
GET /lijun/employee/_search
{
    "query" : {
        "filtered" : {
            #filter
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

#full text match
GET /lijun/employee/_search
{
    "query" : {
        "match" : {
            "about" : "rock climbing"
        }
    }
}

#phrase match
GET /lijun/employee/_search
{
    "query" : {
        "match_phrase" : {
            "about" : "rock climbing"
        }
    }
}



#highlight query outcome
GET /lijun/employee/_search
{
    "query" : {
        "match_phrase" : {
            "about" : "rock climbing"
        }
    },
    "highlight": {
        "fields" : {
            "about" : {}
        }
    }
}

#aggregation
GET /lijun/employee/_search
{
  "aggs": {
    "all_interests": {
      "terms": { "field": "interests" }
    }
  }
}


#multipul aggregation
GET /lijun/employee/_search
{
  "aggs": {
    "all_interests": {
      "terms": { "field": "interests" }
      , "aggs": {
        "avg_age": {
          "avg": {
            "field": "age"
          }
        }
      }
    }
  }
}









