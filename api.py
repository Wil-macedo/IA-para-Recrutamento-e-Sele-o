import os
import joblib
import uvicorn
import numpy as np
import nest_asyncio
from fastapi import FastAPI
from pydantic import BaseModel

# 🔹 Inicializa a API
app = FastAPI(title="API de Previsão com XGBoost")

# 🔹 Carrega o modelo salvo
modelPath = os.path.join(os.getcwd(), 'modelo_xgboost.joblib')
modelo = joblib.load(modelPath)

# 🔹 Define a estrutura dos dados esperados na requisição
class DadosEntrada(BaseModel):
    features: list  # Lista de valores para o modelo

@app.get("/")
def home():
    return {"mensagem": "API de Previsão está rodando! Use /predict para fazer previsões."}

@app.post("/predict")
def predict(dados: DadosEntrada):
    # 🔹 Converte os dados de entrada para array numpy
    X_input = np.array(dados.features).reshape(1, -1)

    # 🔹 Faz a previsão
    previsao = modelo.predict(X_input)

    return {"previsao": int(previsao[0])}  # Retorna a previsão em formato JSON

# Executar a API no Jupyter Notebook
nest_asyncio.apply()
uvicorn.run(app, host="127.0.0.1", port=8000)