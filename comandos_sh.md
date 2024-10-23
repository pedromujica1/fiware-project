## Terminal comands IOT AGENT

curl localhost:1026/v2/entities/<id_entidade> -s -S -H 'Accept: application/json' --header 'fiware-service: smartgondor' --header 'fiware-servicepath: /gardens' | python -mjson.tool

## Listar entidades orion context-broker

curl localhost:1026/v2/entities/ -s -S -H 'Accept: application/json' --header 'fiware-service: smartgondor' --header 'fiware-servicepath: /gardens' | python -mjson.tool

#DELETAR ENTIDADE DO CONTEXT BROKER
curl -X DELETE \
  'http://localhost:1026/v2/entities/<ID_ENTIDADE>' \
  -s -S \
  -H 'Accept: application/json' \
  --header 'fiware-service: smartgondor' \
  --header 'fiware-servicepath: /gardens'

## ESTUDAR INTEGRAÇÃO
- https://www.thethingsindustries.com/docs/integrations/mqtt/

## listar iot agents
curl --location 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /'

## Verificar ultimo dado enviado ao context broker
curl localhost:1026/v2/entities/SensorQualidadeAr_Londrina -s -S -H 'Accept: application/json' --header 'fiware-service: openiot' --header 'fiware-servicepath: /airQuality /' | python3 -mjson.tool