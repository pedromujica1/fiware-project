## Listar entidades orion context-broker

```bash
curl localhost:1026/v2/entities/ -s -S -H 'Accept: application/json' --header 'fiware-service: smartgondor' --header 'fiware-servicepath: /gardens' | python -mjson.tool
```
```bash
#DELETAR ENTIDADE DO CONTEXT BROKER
curl -X DELETE \
  'http://localhost:1026/v2/entities/<ID_ENTIDADE>' \
  -s -S \
  -H 'Accept: application/json' \
  --header 'fiware-service: smartgondor' \
  --header 'fiware-servicepath: /gardens'
```


## listar iot agents
```bash
curl --location 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /'
```

## Verificar ultimo dado enviado ao context broker
```bash
curl localhost:1026/v2/entities/SensorQualidadeAr_Londrina -s -S -H 'Accept: application/json' --header 'fiware-service:openiot' --header 'fiware-servicepath: /airQuality' | python3 -mjson.tool
```
## Caso o Orion não carregue
```bash
sudo docker container prune -f
sudo docker network prune -f
sudo docker compose up -d --force-recreate
```


## Requests FIWARE
https://www.postman.com/fiware/workspace~b6e7fcf4-ff0c-47cb-ada4-e222ddeee5ac/request/j8obq1y/list-all-provisioned-devices

