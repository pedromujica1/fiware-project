#!/bin/bash

# ============================================================
# REGISTRO DO PAXCOUNTER NO FIWARE
# ============================================================

# Localização deste script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Diretório raiz do projeto FIWARE
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Arquivo .env
ENV_FILE="$PROJECT_ROOT/.env"

# ------------------------------------------------------------
# Verifica se o .env existe
# ------------------------------------------------------------

if [ ! -f "$ENV_FILE" ]; then
    echo "Erro: arquivo .env não encontrado:"
    echo "$ENV_FILE"
    exit 1
fi

# Carrega as variáveis
source "$ENV_FILE"

# ------------------------------------------------------------
# Variáveis obrigatórias do PaxCounter
# ------------------------------------------------------------

if [ -z "$PAX_DEVICE_ID" ]; then
    echo "Erro: PAX_DEVICE_ID não definido no .env"
    exit 1
fi

if [ -z "$PAX_ENTITY_NAME" ]; then
    echo "Erro: PAX_ENTITY_NAME não definido no .env"
    exit 1
fi

if [ -z "$PAX_APP_EUI" ]; then
    echo "Erro: PAX_APP_EUI não definido no .env"
    exit 1
fi

if [ -z "$PAX_DEV_EUI" ]; then
    echo "Erro: PAX_DEV_EUI não definido no .env"
    exit 1
fi

if [ -z "$PAX_APPLICATION_ID" ]; then
    echo "Erro: PAX_APPLICATION_ID não definido no .env"
    exit 1
fi

if [ -z "$PAX_APPLICATION_KEY" ]; then
    echo "Erro: PAX_APPLICATION_KEY não definido no .env"
    exit 1
fi

if [ -z "$SERVICE_PATH" ]; then
    echo "Erro: SERVICE_PATH não definido no .env"
    exit 1
fi

# ------------------------------------------------------------
# Registro no IoT Agent LoRaWAN
# ------------------------------------------------------------

echo "=============================================="
echo " REGISTRO DO PAXCOUNTER NO FIWARE"
echo "=============================================="
echo
echo "Device ID : $PAX_DEVICE_ID"
echo "Entidade  : $PAX_ENTITY_NAME"
echo "DevEUI    : $PAX_DEV_EUI"
echo "Service   : openiot"
echo "Path      : $SERVICE_PATH"
echo

response=$(curl --silent --write-out "HTTPSTATUS:%{http_code}" \
    --location --request POST 'http://localhost:4041/iot/devices' \
    --header 'fiware-service: openiot' \
    --header "fiware-servicepath: $SERVICE_PATH" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "devices": [
            {
                "device_id": "'"$PAX_DEVICE_ID"'",
                "entity_name": "'"$PAX_ENTITY_NAME"'",
                "entity_type": "LoraDevice",

                "attributes": [
                    {
                        "object_id": "field1",
                        "name": "WiFi",
                        "type": "Number"
                    },
                    {
                        "object_id": "field2",
                        "name": "BLE",
                        "type": "Number"
                    },
                    {
                        "object_id": "field3",
                        "name": "Pax",
                        "type": "Number"
                    }
                ],

                "internal_attributes": {
                    "lorawan": {
                        "application_server": {
                            "host": "'"$APP_SERVER_HOST"'",
                            "username": "'"$APP_SERVER_USERNAME"'",
                            "password": "'"$APP_SERVER_PASSWORD"'",
                            "provider": "'"$PROVIDER"'"
                        },
                        "app_eui": "'"$PAX_APP_EUI"'",
                        "dev_eui": "'"$PAX_DEV_EUI"'",
                        "application_id": "'"$PAX_APPLICATION_ID"'",
                        "application_key": "'"$PAX_APPLICATION_KEY"'",
                        "data_model": "'"$DATA_MODEL"'"
                    }
                }
            }
        ]
    }')

# ------------------------------------------------------------
# Trata resposta
# ------------------------------------------------------------

body=$(echo "$response" | sed -e 's/HTTPSTATUS\:.*//g')
status=$(echo "$response" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

echo

if [ "$status" -ne 201 ]; then
    echo "Erro ao registrar o PaxCounter."
    echo "HTTP Status: $status"
    echo
    echo "Resposta do servidor:"
    echo "$body"
    exit 1
else
    echo "PaxCounter registrado com sucesso no FIWARE!"
    echo
    echo "HTTP Status: $status"
fi
