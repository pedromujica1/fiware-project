import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import random

# ==========================
# Configurações do Broker
# ==========================
BROKER_HOST = "192.168.122.1"
BROKER_PORT = 1883

USERNAME = "pedromujica1"
PASSWORD = "micelinus536"  # senha vazia

CLIENT_ID = "python-mqtt-publisher"

TOPIC = "airQuality/data"  # ajuste se necessário

PUBLISH_INTERVAL = 5  # segundos

# ==========================
# Callbacks
# ==========================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao broker MQTT")
    else:
        print(f"❌ Erro de conexão. Código: {rc}")

def on_disconnect(client, userdata, rc):
    print("🔌 Desconectado do broker MQTT")

# ==========================
# Cliente MQTT
# ==========================
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

# ==========================
# Conexão
# ==========================
try:
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    while True:
        now = datetime.now()

        payload = {
            "temperatura": round(random.uniform(20.0, 30.0), 2),
            "umidade": round(random.uniform(40.0, 80.0), 2),
            "data": now.strftime("%Y-%m-%d"),
            "hora": now.strftime("%H:%M:%S")
        }

        result = client.publish(
            TOPIC,
            json.dumps(payload),
            qos=0,
            retain=False
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print("📤 Publicado:", payload)
        else:
            print("❌ Falha ao publicar")

        time.sleep(PUBLISH_INTERVAL)

except KeyboardInterrupt:
    print("\n🛑 Encerrando publicação MQTT...")
    client.loop_stop()
    client.disconnect()

except Exception as e:
    print("❌ Erro geral")
    print(e)
