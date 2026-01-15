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
# Cliente MQTT
# ==========================
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# ==========================
# Conexão
# ==========================
try:
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()

except KeyboardInterrupt:
    print("\n🛑 Encerrando subscriber MQTT...")
    client.disconnect()

except Exception as e:
    print("❌ Erro geral")
    print(e)