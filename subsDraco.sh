curl --location 'http://localhost:1026/v2/subscriptions/' \
--header 'Content-Type: application/json' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /airQuality' \
--data '{
  "description": "Notify Draco of all context changes",
  "subject": {
    "entities": [
      {
        "idPattern": ".*"
      }
    ]
  },
  "notification": {
    "http": {
      "url": "http://draco:5050/v2/notify"
    }
  },
  "throttling": 5
}'


curl -X GET \
  'http://localhost:1026/v2/subscriptions/' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /airQuality'