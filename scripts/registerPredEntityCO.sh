#!/bin/bash

response=$(curl --silent --write-out "HTTPSTATUS:%{http_code}" \
--location --request POST 'http://localhost:1026/v2/entities' \
--header 'fiware-service: openiot' \
--header "fiware-servicepath: $SERVICE_PATH" \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "CorrecaoCO",
    "type": "AirQualitySensor",
    "best_co": {
        "type": "Float",
        "value": 0.0
    },
    "co_ae": {
        "type": "Float",
        "value": 0.0
    },
    "co_we": {
        "type": "Float",
        "value": 0.0
    },
    "Temperatura": {
        "type": "Float",
        "value": 0.0
    },
    "Umidade": {
        "type": "Float",
        "value": 0.0
    },
    "co_corrigido": {
        "type": "Float",
        "value": 0.0
    }
}')

# Process response (same as before)
body=$(echo "$response" | sed -e 's/HTTPSTATUS\:.*//g')
status=$(echo "$response" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

[ "$status" -eq 201 ] && echo "Entity created successfully!" || echo "Error: HTTP $status - $body"