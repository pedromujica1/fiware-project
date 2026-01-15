
import requests
import paho.mqtt.client as mqtt
import json

# ==========================
# Configurações do Broker
# ==========================
BROKER_HOST = "192.168.122.1"
BROKER_PORT = 1883

USERNAME = "pedromujica1"
PASSWORD = "micelinus536"  # senha vazia

CLIENT_ID = "python-mqtt-subscriber"

TOPIC = "airQuality/data"  # mesmo tópico do publisher

# ==========================
# Callbacks
# ==========================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao broker MQTT")
        client.subscribe(TOPIC)
        print(f"📡 Inscrito no tópico: {TOPIC}")
    else:
        print(f"❌ Falha na conexão. Código: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("📥 Mensagem recebida:")
        print(payload)
    except json.JSONDecodeError:
        print("📥 Payload recebido (texto):", msg.payload.decode())

def on_disconnect(client, userdata, rc):
    print("🔌 Desconectado do broker MQTT")


    


# ==========================
# Configurações
# ==========================
IOT_AGENT_URL = "http://localhost:4041/iot/devices"

HEADERS = {
    "fiware-service": "openiot",
    "fiware-servicepath": "/airQuality",
    "Content-Type": "application/json"
}

# ==========================
# Identificação do dispositivo
# ==========================
DEVICE_ID = "teste2"
ENTITY_NAME = "agente2"
ENTITY_TYPE = "LoraDevice"

# ==========================
# Configuração LoRaWAN / TTN
# ==========================
APP_SERVER_HOST = "mosquitto:1883"
APP_SERVER_USERNAME = "pedromujica1"
APP_SERVER_PASSWORD = "micelinus536"

APP_EUI = "localApp"
DEV_EUI = "123456789"
APPLICATION_ID = "demoLocal"
APPLICATION_KEY = "micelinus536"
DATA_MODEL = "application_server"

# ==========================
# Payload (ATRIBUTOS REDUZIDOS)
# ==========================
payload = {
    "devices": [
        {
            "device_id": DEVICE_ID,
            "entity_name": ENTITY_NAME,
            "entity_type": ENTITY_TYPE,
            "attributes": [
                {"object_id": "temperatura", "name": "Temperatura", "type": "Float"},
                {"object_id": "umidade", "name": "Umidade", "type": "Float"},
                {"object_id": "data", "name": "DATA", "type": "Text"},
                {"object_id": "hora", "name": "HORA", "type": "Text"}
            ],
            "internal_attributes": {
                "lorawan": {
                    "application_server": {
                        "host": APP_SERVER_HOST,
                        "username": APP_SERVER_USERNAME,
                        "password": APP_SERVER_PASSWORD,
                        "provider": "json"
                    },
                    "app_eui": APP_EUI,
                    "dev_eui": DEV_EUI,
                    "application_id": APPLICATION_ID,
                    "application_key": APPLICATION_KEY,
                    "data_model": DATA_MODEL
                }
            }
        }
    ]
}

# ==========================
# Envio da requisição
# ==========================
try:
    response = requests.post(
        IOT_AGENT_URL,
        headers=HEADERS,
        json=payload,
        timeout=10
    )

    if response.status_code in (200, 201):
        print("✅ Dispositivo registrado com sucesso!")
    else:
        print("❌ Erro ao registrar dispositivo")
        print("Status:", response.status_code)
        print("Resposta:", response.text)

except requests.exceptions.RequestException as e:
    print("❌ Erro de conexão com o IoT Agent")
    print(e)

