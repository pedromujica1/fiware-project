
import json
import time
import base64
import random
import argparse
from paho.mqtt import client as mqtt_client
from paho.mqtt import client as mqtt_client
from paho.mqtt.client import CallbackAPIVersion


#exemplo de uso
# python3 send-data.py --id_device {}  --interval 1
#10 dispositivos a cada 1 segundo

#config mqtt
BROKER = "localhost"
PORT = 1883
USERNAME = "admin"
PASSWORD = "password"

TOPIC = "v3/demoTTN/devices/{device_id}/up"

#gera os payloads
def generate_payload():
    payload = bytearray()
    
    #campo A - Pressao Barometica
    pressure = random.uniform(980.0, 1030.0)
    #converte para 0.1 hPa
    pressure_lpp = int(pressure * 10)  
    payload.extend([0x00, 0x73])
    payload.extend(pressure_lpp.to_bytes(2, byteorder='big', signed=False))
    
    #campo B de temperatura
    temperature = random.uniform(20.0, 35.0)
    temp_lpp = int(temperature * 10)
    payload.extend([0x01, 0x67])
    payload.extend(temp_lpp.to_bytes(2, byteorder='big', signed=True))
    
    #campo C - umidade relativa
    humidity = random.uniform(30.0, 80.0)
    #converte para 0.5%
    humidity_lpp = int(humidity * 2)  
    payload.extend([0x02, 0x68])
    payload.extend(humidity_lpp.to_bytes(1, byteorder='big'))
    
    #campo d - fica fixo
    #Canal 0x03 | Tipo 0x00 | Valor 0x64
    payload.extend([0x03, 0x00, 0x64])
    
    #campo e - fica fixo
    #Canal 0x04 | Tipo 0x01 | Valor 0x00
    payload.extend([0x04, 0x01, 0x00])

    #campo F - Mantém fixo
    #Canal 0x05 | Tipo 0x01 | Valor 0xD7 
    payload.extend([0x05, 0x01, 0xD7])
    
    payload_base64 = base64.b64encode(payload).decode()
    print("Payload RAW (Base64):")
    print(payload_base64)
    
    return payload_base64

#retorna indice de device
def device_id(index):
    return f"myDevice{index}"

#cliente mqtt
def connect_mqtt(client_id: str):
    client = mqtt_client.Client(
        client_id=client_id,
        callback_api_version=CallbackAPIVersion.VERSION2
    )
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, PORT)
    return client

#publica os dados
def publish_devices(client, id_device, interval):
    counter = 0
    while True:
        dev_id = device_id(id_device)
        topic = TOPIC.format(device_id=dev_id)

        payload = {
            "app_id": "demoTTN",
            "dev_id": dev_id,
            "hardware_serial": f"{id_device:016x}",
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
    parser.add_argument("--id_device", type=int, default=10, help="dispositivos inicias")
    parser.add_argument("--interval", type=float, default=5, help="Intervalo entre ciclos (segundos)")
    args = parser.parse_args()

    client = connect_mqtt("devices_generator")
    client.loop_start()
    #
    publish_devices(client,args.id_device, args.interval)