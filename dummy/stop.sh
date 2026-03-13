##!/usr/bin/env bash

curl --location --request DELETE 'localhost:4041/iot/services?resource=70B3D57ED00006B2&apikey=' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /airQuality'


curl --location --request DELETE 'localhost:4041/iot/devices/myDevice' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /airQuality'

docker compose down -v

curl --location 'http://localhost:1026/v2/subscriptions' \
--header 'Content-Type: application/json' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /airQuality' \
--data '{
  "description": "Notify Cygnus only sensor attrs",
  "subject": {
    "entities": [
      {
        "idPattern": ".*",
        "type": "WeatherObserved"
      }
    ],
    "condition": {
      "attrs": [
        "temperature",
        "pressure",
        "relative_humidity"
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5055/notify"
    },
    "attrs": [
      "temperature",
      "pressure",
      "relative_humidity"
    ],
    "onlyChangedAttrs": true
  },
  "throttling": 0
}'

curl -X DELETE \ http://localhost:1026/v2/subscriptions/65d8a3f3c0a9e3d1f9d12345 \
-H "Fiware-Service: openiot" \
-H "Fiware-ServicePath: /airQuality"