
import os
import boto3  # Use in MLFLOW.
import mlflow
import joblib
import requests
import pandas as pd
from xgboost import XGBClassifier
from application.libs.pre_processing_model import pre_processing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_model():
    try:
        # Create a new MLflow Experiment
        
        print("STARTING - train_model()")
        
        try:
            mlFlow_url:str = None
            # URL pode variar dependendo do ambiente, se está rodando com docker compose ou em container isolados.
            for url in ("http://localhost:5000", "http://mlflow-app:5000"):
                
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    mlFlow_url = url
            
            if mlFlow_url is not None:
                mlflow.set_tracking_uri(uri=mlFlow_url)
        except Exception as ex:
            print("FALHA MLFLOW :(") 
            
        mlflow.set_experiment("MLflow Recrutamento & seleção")

        df_X_no_outliers, df_Y_no_outliers = pre_processing()

        if df_X_no_outliers is None or df_Y_no_outliers is None:
            return "FALHA NO PROCESSAMENTO DOS DADOS"

        X_train, X_test, y_train, y_test = train_test_split(
            df_X_no_outliers, df_Y_no_outliers, test_size=0.2, random_state=42)

        with mlflow.start_run():

            _parameters = {
                'learning_rate': 0.3,
                'max_depth': 7,
                'n_estimators': 150}

            # 🔹 Criando e treinando o modelo XGBoost
            model = XGBClassifier(
                eval_metric="logloss",
                learning_rate=_parameters['learning_rate'],
                max_depth=_parameters['max_depth'],
                n_estimators=_parameters['n_estimators']
            )

            model.fit(X_train, y_train)

            # 🔹 Fazendo previsões
            y_pred = model.predict(X_test)

            # 🔹 Avaliação do modelo
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)

            print(f"Acurácia: {accuracy:.2%}")
            print("Relatório de Classificação:\n", report)

            # 🔹 Fazer previsões no conjunto de validação
            y_val_pred = model.predict(X_test)

            # 🔹 Avaliar desempenho
            accuracy = accuracy_score(y_test, y_val_pred)
            print(f"Acurácia no conjunto de validação: {accuracy:.2%}")

            # Forneça um exemplo de entrada para o MLflow
            input_example = pd.DataFrame(X_train.iloc[[0]]) if isinstance(
                X_train, pd.DataFrame) else X_train[0:1]
            mlflow.sklearn.log_model(
                model,
                "modelo_xgboost.joblib",
                input_example=input_example)

            # 🔹 Salvando o modelo em disco.
            joblib.dump(model, "modelo_xgboost.joblib")

        return f"MODEL TRAINED = ACCURACY:{accuracy:.2%}"

    except Exception as ex:
        print("@ ERRO @")
        return str(ex)

if __name__ == "__main__":
    train_model()