## Listar entidades orion context-broker

curl localhost:1026/v2/entities/ -s -S -H 'Accept: application/json' --header 'fiware-service: smartgondor' --header 'fiware-servicepath: /gardens' | python -mjson.tool

#DELETAR ENTIDADE DO CONTEXT BROKER
curl -X DELETE \
  'http://localhost:1026/v2/entities/<ID_ENTIDADE>' \
  -s -S \
  -H 'Accept: application/json' \
  --header 'fiware-service: smartgondor' \
  --header 'fiware-servicepath: /gardens'


## listar iot agents
curl --location 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /'

## Verificar ultimo dado enviado ao context broker
curl localhost:1026/v2/entities/SensorQualidadeAr_Londrina -s -S -H 'Accept: application/json' --header 'fiware-service: openiot' --header 'fiware-servicepath: /airQuality /' | python3 -mjson.tool

## Requests FIWARE
https://www.postman.com/fiware/workspace~b6e7fcf4-ff0c-47cb-ada4-e222ddeee5ac/request/j8obq1y/list-all-provisioned-devices