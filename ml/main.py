#Bibliotecas FastAPI
from fastapi import FastAPI, HTTPException
import httpx,json
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta


#Bibliotecas de Machine Learning
import sys
import warnings
from typing import Dict, List, Optional, Tuple, Union
from itertools import product

#Third-party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Scientific computing
from scipy import stats
from scipy.stats import uniform, randint


# Machine Learning
from sklearn import __version__ as sklearn_version
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
# from sklearn.neural_network import MLPRegressor
# from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    RandomizedSearchCV,
    RepeatedKFold,
    cross_val_score,
    cross_validate
)
import pickle
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error
)


app = FastAPI(title="API para correção de dados da Estação Envcity")

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

#salvando arquivo de RandomForest Regressor
with open("RF_Regressor.pickle", "rb") as f:
    modelo = pickle.load(f)

ORION_URL = "http://localhost:1026/v2/subscriptions"
FIWARE_SERVICE = "openiot"
FIWARE_SERVICEPATH = "/airQuality"


@app.get("/")
def read_root():
    return {"Welcome to my API!": "Fiware greetings"}


#listar todas as entidades do context broker
@app.get("/entidadesLista")
async def getOrionEntities():
    orion_url = "http://localhost:1026/v2/entities/"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                orion_url,
                headers={
                    "Accept": "application/json",
                    "fiware-service": "openiot",
                    "fiware-servicepath": "/airQuality"
                }
            )
            response.raise_for_status()
            return JSONResponse(content=response.json())
            
    except httpx.HTTPStatusError as e:
        return JSONResponse(
            content={"error": f"Orion request failed: {str(e)}"},
            status_code=e.response.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Unexpected error: {str(e)}"},
            status_code=500
        )

@app.post("/test-orion-connection")
async def test_orion():
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("http://localhost:1026/version")
            return {"status": "success", "orion_version": r.text}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

#inscrição para receber info do sensor-cvel
@app.post("/notification")
async def create_subscription(notification_url: str = "http://localhost:8000/"):
    """
    Cria uma subscription no Orion para todos os atributos do SensorCvel
    """
    subscription_payload = {
        "description": "Subscription for all SensorCvel attributes",
        "subject": {
            "entities": [{"id": "SensorCvel", "type": "LoraDevice"}],
            "condition": {
                "attrs": [
                    "Best_CO", "Best_NO2", "Best_OX", "Best_SO2",
                    # ... (todos os outros atributos)
                ]
            }
        },
        "notification": {
            "http": {
                "url": notification_url,
                "accept": "application/json"
            },
            "attrs": [
                "Best_CO", "Best_NO2", "Best_OX", "Best_SO2",
                # ... (todos os outros atributos)
            ]
        },
        "expires": "2040-01-01T14:00:00.00Z",
        "throttling": 1
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                ORION_URL,
                headers={
                    "Content-Type": "application/json",
                    "fiware-service": FIWARE_SERVICE,
                    "fiware-servicepath": FIWARE_SERVICEPATH
                },
                json=subscription_payload
            )
            
            # Debug: Log da resposta bruta
            print(f"Orion response status: {response.status_code}")
            print(f"Orion response text: {response.text}")
            
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=500,
                    detail=f"Orion returned invalid JSON: {response.text}"
                )
                
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail={
                        "orion_error": response_json,
                        "sent_payload": subscription_payload
                    }
                )
                
            return JSONResponse(content=response_json, status_code=201)
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Connection to Orion failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

    
@app.post("/prediction")
async def calculate_prediction():
    pass

    

# #requisição para ouvir notificações context broker
# @app.post("/subscribe")
# async def subscribe_lora_device():
#     orion_url = "http://localhost:1026/v2/subscriptions"

#     headers = {
#         "Content-Type": "application/json"
#     }

#     entity_id = "sensor001"  #alterar o nome dependendo
#     entity_type = "LoraDevice"
#     notify_url = "http://host.docker.internal:3003/predict"

#     attributes_to_watch = [
#         "Best_CO", "Best_NO2", "Best_OX", "Temperatura", "Umidade"
#     ]

#     subscription_payload = {
#         "description": f"Subscription for entity {entity_id}",
#         "subject": {
#             "entities": [
#                 {
#                     "id": entity_id,
#                     "type": entity_type
#                 }
#             ],
#             "condition": {
#                 "attrs": attributes_to_watch
#             }
#         },
#         "notification": {
#             "http": {
#                 "url": notify_url
#             },
#             "attrs": attributes_to_watch
#         },
#         "expires": "2040-01-01T14:00:00.00Z",
#         "throttling": 5
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(orion_url, headers=headers, json=subscription_payload)

#     return {
#         "status_code": response.status_code,
#         "response": response.json() if response.status_code < 400 else response.text
#     }

