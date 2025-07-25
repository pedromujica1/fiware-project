#Bibliotecas FastAPI
from fastapi import FastAPI, HTTPException, Request
import httpx,json
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

#Third-party imports
import numpy as np
from joblib import load
import pandas as pd
import os

#Modelos Pydantic para input do modelo
class InputData(BaseModel):
    e2sp_co: float
    e2sp_co_we: float
    e2sp_co_ae: float
    e2sp_temp: float
    pin_umid: float

class PredictionResult(BaseModel):
    CO_previsto: float 

app = FastAPI(title="API para correção de dados da Estação Envcity")

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


#Carregando modelo
model_path = os.path.join(os.path.dirname(__file__), 'RF_Regressor.joblib')
modelo = load('RF_Regressor.joblib') 


ORION_BASE_URL = os.getenv("ORION_BASE_URL", "http://0.0.0.0:1026")
ORION_ENTITIES_URL = f"{ORION_BASE_URL}/v2/entities/"
ORION_SUBSCRIPTIONS_URL = f"{ORION_BASE_URL}/v2/subscriptions"
ORION_VERSION_URL = f"{ORION_BASE_URL}/version"


FIWARE_SERVICE = "openiot"
FIWARE_SERVICEPATH = "/airQuality"

ORION_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "fiware-service": FIWARE_SERVICE,
    "fiware-servicepath": FIWARE_SERVICEPATH
}

ORION_GET_HEADERS = {
    "Accept": "application/json",
    "fiware-service": "openiot",
    "fiware-servicepath": "/airQuality"
}
# ==============================

#para fazer GET request com o httpx
async def async_request(url: str, headers: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(ORION_ENTITIES_URL, headers=ORION_GET_HEADERS)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return erro_orion(e)
    except Exception as e:
        return erro_interno(e)
    
#Conexão ORION erro
def erro_orion(e: httpx.HTTPStatusError):
    return JSONResponse(
        content={"error": f"Falha na requisição ao Orion: {str(e)}"},
        status_code=e.response.status_code
    )
#erro interno
def erro_interno(e: Exception):
    return JSONResponse(
        content={"error": f"Erro inesperado: {str(e)}"},
        status_code=500
    )

@app.get("/",tags=['Welcome!!'])
def welcome():
    return {"status_code": "200",
            "description": "IT WORKS!"}

#lista entidade do orion CB
@app.get("/orion/entities", summary="📄 Listar Entidades do Orion",tags=['Orion CB operations'])
async def listar_entidades_orion():
    try:
        entidades = await async_request(ORION_ENTITIES_URL, headers=ORION_GET_HEADERS)
        return JSONResponse(content=entidades)
    except httpx.HTTPStatusError as e:
        return erro_orion(e)
    except Exception as e:
        return erro_interno(e)

#testa conexão
@app.get("/orion/status", summary="🔗 Testar Conexão com Orion",tags=['Orion CB operations'])
async def testar_conexao():
    resultado = await async_request(ORION_VERSION_URL,headers=ORION_HEADERS)
    return {"status": "Conectado com sucesso!", "versão_orion": resultado}

#request de predição com base no modelo carregado
@app.post("/prediction", response_model=PredictionResult, tags=['Prediction'])
async def calculate_prediction(data: InputData):
    
    #Constrói o vetor de entrada
    entrada = pd.DataFrame([[data.e2sp_co, data.e2sp_co_we, data.e2sp_co_ae, data.e2sp_temp, data.pin_umid]],columns=['e2sp_co', 'e2sp_co_we', 'e2sp_co_ae', 
    'e2sp_temp', 'pin_umid'])  # Use os mesmos nomes do treino # 1 amostra, 5 features calculados pelo numpy

    # Realiza a predição
    resultado = modelo.predict(entrada)

    return PredictionResult(CO_previsto=resultado[0])

#cria inscrição orion fazer o POST quando entidade SensorCvel atualiza
@app.post("/orion/subscribe", summary="📡 Notificar quando SensorCvel atualizar", tags=['Notification'])
async def orion_subscripton():
    ORION_SUBSCRIPTION_URL = f"{ORION_BASE_URL}/v2/subscriptions"
    API_SERVICE_NAME = "ml-api"
    PREDICTION_ENDPOINT = f"http://{API_SERVICE_NAME}:8000/notifyCO"
    
    headers = {"Content-Type": "application/json","Content-Type": "application/json",
    "fiware-service": FIWARE_SERVICE,
    "fiware-servicepath": FIWARE_SERVICEPATH}
    payload = {
        "description": "Subscribe to SensorCvel updates",
        "subject": {
            "entities": [
                {
                    "id": "SensorCvel",
                    "type": "LoraDevice"
                }
            ],
            "condition": {
                "attrs": ["Best_CO", "CO_WE", "CO_AE", "Temperatura", "Umidade"]
            }
        },
        "notification": {
            "http": {
                "url": PREDICTION_ENDPOINT
            },
            "attrs": ["Best_CO", "CO_WE", "CO_AE", "Temperatura", "Umidade"]
        },
        "throttling": 1
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(ORION_SUBSCRIPTION_URL, json=payload, headers=headers)
            response.raise_for_status()
            if response.status_code == 201:
                return {"status": "Subscription criada com sucesso!"}
            return {"status": "Subscription resposta recebida", "content": response.text}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/notifyCO", summary="🌐 Encaminha valor corrigido para Orion CB", tags=['Notification'])
async def co_prediction(req: Request):
    body = await req.json()
    
    
    #Extração do JSON Orion
    data = body.get("data", [])[0]
    #retirada dos campos necessarios
    e2sp_co = data.get("Best_CO", {}).get("value", 0.0)
    e2sp_co_we = data.get("CO_WE", {}).get("value", 0.0)
    e2sp_co_ae = data.get("CO_AE", {}).get("value", 0.0)
    e2sp_temp = data.get("Temperatura", {}).get("value", 0.0)
    pin_umid = data.get("Umidade", {}).get("value", 0.0)

    entrada = pd.DataFrame([[data.e2sp_co, data.e2sp_co_we, data.e2sp_co_ae, data.e2sp_temp, data.pin_umid]],columns=['e2sp_co', 'e2sp_co_we', 'e2sp_co_ae', 
    'e2sp_temp', 'pin_umid'])
    #predição!!!
    resultado = modelo.predict(entrada)
    #corpo para atualizar lá no patch
    payload_CO = {
            "CO_Corrigido": {
                "type": "Float",
                "value": resultado[0]  # sem arredondar
            }
    }
    #enviando para o Orion CB
    async with httpx.AsyncClient() as client:
        linha_req = f"http://{ORION_BASE_URL}/v2/entities/SensorCvel/attrs"
        response = await client.patch(linha_req, json=payload_CO, headers=ORION_HEADERS)
        response.raise_for_status()

    return {"status": "Enviado para o Orion CB!", "co_corrigido": resultado[0]}
