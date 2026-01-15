import json
import time
import base64
import random
import string
import argparse
from paho.mqtt import client as mqtt_client

#config mqtt
BROKER = "localhost"
PORT = 1883
USERNAME = "pedromujca1"
PASSWORD = "micelinus536"

TOPIC = "v3/demoTTN/devices/{device_id}/up"

#gera os payloads
def generate_payload():
    """
    Simula um payload binário e codifica em Base64
    """
    raw_bytes = bytes([
        random.randint(0, 255),  # temperatura
        random.randint(0, 255),  # umidade
        random.randint(0, 255),  # pressão
        random.randint(0, 255)
    ])
    return base64.b64encode(raw_bytes).decode()

#retorna indice de device
def device_id(index):
    return f"myDevice{index}"

#cliente mqtt
def connect_mqtt(client_id):
    client = mqtt_client.Client(client_id=client_id)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, PORT)
    return client

#publica os dados
def publish_devices(client, num_devices, interval):
    counter = 0

    while True:
        for i in range(1, num_devices + 1):
            dev_id = device_id(i)
            topic = TOPIC.format(device_id=dev_id)

            payload = {
                "app_id": "demoTTN",
                "dev_id": dev_id,
                "hardware_serial": f"{i:016x}",
                "port": 1,
                "counter": counter,
                "is_retry": False,
                "confirmed": False,
                "payload_raw": generate_payload()
            }

            client.publish(topic, json.dumps(payload))
            print(f"[PUB] {topic} -> counter={counter}")

        counter += 1
        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FIWARE LoRaWAN Scalability Test")
    parser.add_argument("--devices", type=int, default=10, help="Número de dispositivos")
    parser.add_argument("--interval", type=float, default=5, help="Intervalo entre ciclos (segundos)")
    args = parser.parse_args()

    client = connect_mqtt("devices_generator")
    client.loop_start()

    publish_devices(client, args.devices, args.interval)
