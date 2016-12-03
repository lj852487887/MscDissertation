#command on the cluster

#check elastcisearch server
curl -X GET '10.1.2.3:9200'   

curl '10.1.2.3:9200/?pretty'

#show all indices of es server
curl '10.1.2.3:9200/_cat/indices?v'