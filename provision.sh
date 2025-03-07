#!/bin/sh
curl --location --request POST 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /airQuality' \
--header 'Content-Type: application/json' \
--data-raw '{
    "devices": [
        {
            "device_id": "env1",
            "entity_name": "SensorQualidadeAr_Londrina",
            "entity_type": "LoraDevice",
            "attributes": [
                { "object_id": "best_co", "name": "Best_CO", "type": "Float"},
                { "object_id": "best_no2", "name": "Best_NO2", "type": "Float"},
                { "object_id": "best_ox", "name": "Best_OX", "type": "Float"},
                { "object_id": "best_so2", "name": "Best_SO2", "type": "Float"},
                { "object_id": "co_1", "name": "CO_1", "type": "Float"},
                { "object_id": "co_2", "name": "CO_2", "type": "Float"},
                { "object_id": "co_3", "name": "CO_3", "type": "Float"},
                { "object_id": "co_4", "name": "CO_4", "type": "Float"},
                { "object_id": "co_ae", "name": "CO_AE", "type": "Float"},
                { "object_id": "co_we", "name": "CO_WE", "type": "Float"},
                { "object_id": "no2_1", "name": "NO2_1", "type": "Float"},
                { "object_id": "no2_2", "name": "NO2_2", "type": "Float"},
                { "object_id": "no2_3", "name": "NO2_3", "type": "Float"},
                { "object_id": "no2_4", "name": "NO2_4", "type": "Float"},
                { "object_id": "no2_ae", "name": "NO2_AE", "type": "Float"},
                { "object_id": "no2_we", "name": "NO2_WE", "type": "Float"},
                { "object_id": "ox_1", "name": "OX_1", "type": "Float"},
                { "object_id": "ox_2", "name": "OX_2", "type": "Float"},
                { "object_id": "ox_3", "name": "OX_3", "type": "Float"},
                { "object_id": "ox_4", "name": "OX_4", "type": "Float"},
                { "object_id": "ox_ae", "name": "OX_AE", "type": "Float"},
                { "object_id": "ox_we", "name": "OX_WE", "type": "Float"},
                { "object_id": "so2_1", "name": "SO2_1", "type": "Float"},
                { "object_id": "so2_2", "name": "SO2_2", "type": "Float"},
                { "object_id": "so2_3", "name": "SO2_3", "type": "Float"},
                { "object_id": "so2_4", "name": "SO2_4", "type": "Float"},
                { "object_id": "so2_ae", "name": "SO2_AE", "type": "Float"},
                { "object_id": "so2_we", "name": "SO2_WE", "type": "Float"},
                { "object_id": "Temperatura", "name": "Temperatura", "type": "Float"},
                { "object_id": "Umidade", "name": "Umidade", "type": "Float"},
                { "object_id": "data", "name": "DATA", "type": "Text"},
                { "object_id": "hora", "name": "HORA", "type": "Text"}
            ],
            "internal_attributes": {
                "lorawan": {
                    "application_server": {
                        "host": "au1.cloud.thethings.network",
                        "username": "envcity-aqm@ttn",
                        "password": "",
                        "provider": "TTN"
                    },
                    "app_eui": "1231231231231231",
                    "dev_eui": "70B3D57ED00678EB",
                    "application_id": "envcity-aqm@ttn",
                    "application_key": "E078A5F764CFA112E6BA26496CA19A5B",
                    "data_model": "application_server"
                }
            }
        }
    ]
}'

curl --location --request POST 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /airQuality' \
--header 'Content-Type: application/json' \
--data-raw '{
    "devices": [
        {
            "device_id": "tbeam-v1",
            "entity_name": "PaxCounter",
            "entity_type": "LoraDevice",
            "attributes": [
                { "object_id": "field1", "name": "Field1", "type": "Number" },
                { "object_id": "field2", "name": "Field2", "type": "Number" },
                { "object_id": "field3", "name": "Field3", "type": "Number" }
            ],
            "internal_attributes": {
                "lorawan": {
                    "application_server": {
                        "host": "au1.cloud.thethings.network:1883",
                        "username": "paxcounter-unioeste@ttn",
                        "password": "NNSXS.XSKVQMYGSW5W3GFRPRZHNF57TORL5OQMGQEFXSY.CZTPTDXWFK7NHFOK4SVSBRMFKKKYHGZMPQL2WDZZAXY26EMLSZWQ",
                        "provider": "TTN"
                    },
                    "app_eui": "70B3D57ED006A5A4",
                    "dev_eui": "70B3D57ED006A5A4",
                    "application_id": "paxcounter-unioeste@ttn",
                    "application_key": "NNSXS.XSKVQMYGSW5W3GFRPRZHNF57TORL5OQMGQEFXSY.CZTPTDXWFK7NHFOK4SVSBRMFKKKYHGZMPQL2WDZZAXY26EMLSZWQ",
                    "data_model": "application_server"
                }
            }
        }
    ]
}'
