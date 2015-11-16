curl -XPUT localhost:9200/dazai-demo --data-binary @analyze.json 
curl -XPOST localhost:9200/_bulk --data-binary @ningen.json
