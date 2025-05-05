import os
import joblib
from sklearn.base import ClassifierMixin


def load_model() -> ClassifierMixin:
    "Load model"
    try:
        paths = [
            os.path.join("app","model", 'modelo_xgboost.joblib'),
            os.path.join("model", 'modelo_xgboost.joblib')
        ]
        
        for path in paths:
            if os.path.exists(path):
                model = joblib.load(path)
            else:
                print("NOT EXISTS: {path}")
    
    except Exception as ex:
        print(f"Erro: Arquivo de modelo não encontrado em: {path}")
        model = None  # Garante que 'modelo' esteja definido mesmo se o arquivo não for encontrado
 
    return model