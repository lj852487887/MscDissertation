#command on the cluster
#
#

#check all ssh tunnels
ps aux | grep ssh

#check net port
netstat -tunlp

#check elastcisearch server
curl -X GET '10.1.2.3:9200'   

curl '10.1.2.3:9200/?pretty'

#show all indices of es server
curl '10.1.2.3:9200/_cat/indices?v'

#check cluster state
curl -XGET 'http://se003:9200/_cluster/state?pretty'  

curl -XGET 'http://se003:9200/_nodes?pretty'


#count all indices
curl -XGET 'http://se003:9200/_count?pretty' -d '
{
    "query": {
        "match_all": {}
    }
}'