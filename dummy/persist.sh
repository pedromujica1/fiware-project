#!/bin/bash
echo 'persisting dummy device data'

# Faz a requisição de criação de subscription
curl --location 'http://localhost:1026/v2/subscriptions/' \
--header 'Content-Type: application/json' \
--header 'fiware-service: openiot' \
--header "fiware-servicepath: /airQuality" \
--data '{
  "description": "Notify Cygnus of all context changes",
  "subject": {
    "entities": [
      {
        "idPattern": ".*"
      }
    ]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5055/notify"
    }
  },
  "throttling": 5
}'