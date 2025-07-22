from fastapi import FastAPI
import httpx
#Bibliotecas de Machine Learning

import sys
import warnings
from typing import Dict, List, Optional, Tuple, Union
from itertools import product

# Third-party imports
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

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

#requisição para ouvir notificações context broker
@app.post("/subscribe")
async def subscribe_lora_device():
    orion_url = "http://localhost:1026/v2/subscriptions"

    headers = {
        "Content-Type": "application/json"
    }

    entity_id = "sensor001"  #alterar o nome dependendo
    entity_type = "LoraDevice"
    notify_url = "http://host.docker.internal:3003/predict"

    attributes_to_watch = [
        "Best_CO", "Best_NO2", "Best_OX", "Temperatura", "Umidade"
    ]

    subscription_payload = {
        "description": f"Subscription for entity {entity_id}",
        "subject": {
            "entities": [
                {
                    "id": entity_id,
                    "type": entity_type
                }
            ],
            "condition": {
                "attrs": attributes_to_watch
            }
        },
        "notification": {
            "http": {
                "url": notify_url
            },
            "attrs": attributes_to_watch
        },
        "expires": "2040-01-01T14:00:00.00Z",
        "throttling": 5
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(orion_url, headers=headers, json=subscription_payload)

    return {
        "status_code": response.status_code,
        "response": response.json() if response.status_code < 400 else response.text
    }


#requisição para criar nova entidade
#requisição predict nos dados da TTN



@app.get("/")
def read_root():
    return {"Hello": "World"}
