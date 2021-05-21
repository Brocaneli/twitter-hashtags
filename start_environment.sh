docker build -t brocaneli/twitter-hashtags:latest . 
docker-compose up -d
echo "Waiting for web application to start" && sleep 30
echo "API is up, waiting for Kibana" && sleep 30
curl 'http://localhost:5601/api/saved_objects/index-pattern' \
  -H 'Connection: keep-alive' \
  -H 'kbn-version: 7.12.1' \
  -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36' \
  -H 'Content-Type: application/json' \
  -H 'Accept: */*' \
  -H 'Origin: http://localhost:5601' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: http://localhost:5601/app/management/kibana/indexPatterns/create' \
  -H 'Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6,fr-FR;q=0.5,fr;q=0.4' \
  -H 'Cookie: grafana_session=7dc2c05b317b7fa65fb354a3487f2ae9' \
  --data-binary '{"attributes":{"fieldAttrs":"{}","title":"logstash*","timeFieldName":"@timestamp","fields":"[]","runtimeFieldMap":"{}"}}' \
  --compressed
