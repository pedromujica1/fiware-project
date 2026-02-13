import requests
import json

device = "myDevice1"
entidade = f"urn:WeatherObserved:{device}"
ORION_URL = f"http://localhost:1026/v2/entities/{entidade}"

HEADERS = {
    "fiware-service": "openiot",
    "fiware-servicepath": "/airQuality"
}

response = requests.get(ORION_URL, headers=HEADERS)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Erro {response.status_code}")
    print(response.text)