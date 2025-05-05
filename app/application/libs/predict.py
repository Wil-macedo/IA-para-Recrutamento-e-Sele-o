import os
import joblib
import pandas as pd
from .load_model import load_model
from sklearn.preprocessing import LabelEncoder, StandardScaler

selected_features = [
    'sexo',
    'nivel_ingles_candidato',
    'tipo_contratacao',
    'prioridade_vaga',
    'origem_vaga',
    'nivel_profissional_vaga',
    'nivel_academico_vaga',
    'nivel_ingles_vaga',
    'nivel_espanhol_vaga',
    'areas_atuacao_vaga']

# EXAMPLE
# input_parameters = [
#         "Masculino",
#         "Avançado",
#         "PJ/Autônomo",
#         "Média: Média complexidade 6 a 10 dias",
#         "Nova Posição",
#         "Sênior",
#         "Ensino Médio Completo",
#         "Nenhum",
#         "Nenhum",
#         "Gestão e Alocação de Recursos de TI-"
#         ]


def predict_model(info: dict) -> str:
    "Return a predict result"
    global selected_features

    try:
        model = load_model()

        input_parameters = [
            info['sexo'],
            info['nivel_ingles_candidato'],
            info['tipo_contratacao'],
            info['prioridade_vaga'],
            info['origem_vaga'],
            info['nivel_profissional_vaga'],
            info['nivel_academico_vaga'],
            info['nivel_ingles_vaga'],
            info['nivel_espanhol_vaga'],
            info['areas_atuacao_vaga']
        ]

        folder_name = "files"
        file_name_scaler = os.path.join(folder_name, "scaler.pkl")

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        nova_entrada_df = pd.DataFrame(
            [input_parameters], columns=selected_features)

        # ------------------------------------------------------------ #

        for coluna in selected_features:
            file_path = os.path.join(folder_name, f"LabelEncoder_{coluna}.pkl")
            le_carregado: LabelEncoder = joblib.load(file_path)

            nova_entrada_df[coluna] = le_carregado.transform(
                nova_entrada_df[coluna])

        scaler: StandardScaler = joblib.load(file_name_scaler)
        nova_entrada_normalizada = scaler.fit_transform(nova_entrada_df)

        predict_result = model.predict(nova_entrada_normalizada)

        valor_predito = predict_result[0]

        result = "APROVADO" if valor_predito else "REPROVADO"

        return result

    except Exception as ex:
        return str(ex)
