
import os
import boto3  # Use in MLFLOW.
import joblib
import pandas as pd
from scipy import stats
from .process_files import Files
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, LabelEncoder
from .process_files import processar_json, processar_json_para_dataframe


files_info: dict[str, Files]


def pre_processing():
    df_X_no_outliers: pd.DataFrame = None
    df_Y_no_outliers: pd.DataFrame = None

    try:

        files_info = {
            "applicants": Files("applicants.json"),
            "vagas": Files("vagas.json"),
            "prospects": Files("prospects.json")
        }

        print("ARQUIVOS - OK")
        
        applicants: pd.DataFrame = processar_json(
            files_info.get("applicants").path, "id_candidato")
        vagas: pd.DataFrame = processar_json(
            files_info.get("vagas").path, key="id_vaga")
        prospects: pd.DataFrame = processar_json_para_dataframe(
            files_info.get("prospects").path)

        print("ARQUIVOS CARREGADOS EM DATAFRAME")
        # ------------------------------------------------------------------------------------------------------------- #
        # ------------------------------------------------------------------------------------------------------------- #

        prospects.rename(
            columns={
                'codigo': 'id_candidato',
                'cidade': 'cidade_vaga'},
            inplace=True)

        # Unir Prospects com Applicants (vaga -> candidato)
        prospects_applicants = prospects.merge(
            applicants,
            left_on="id_candidato",
            right_on="id_candidato",
            how="left")

        # Unir com Vagas (vaga -> detalhes da vaga)
        df_original = prospects_applicants.merge(
            vagas,
            left_on="id_vaga",
            right_on="id_vaga",
            how="left")

        # Remover 'nome_y'
        df_original = df_original.drop(columns=['nome_y'], errors='ignore')

        # Renomear colunas
        df_original = df_original.rename(
            columns=lambda col: col.replace(
                '_x', '_candidato').replace(
                    '_y', '_vaga'))

        df_original = df_original.rename(
            columns={
                "local": "cidade_candidato",
                "cidade": "cidade_vaga",
                "nivel profissional": "nivel_profissional_vaga",
                "areas_atuacao": "areas_atuacao_vaga",
                "nivel_profissional": "nivel_profissional_candidato",
                "cursos": "cursos_candidato",
                "remuneracao": "remuneracao_candidato"})

        # Separando as colunas a serem usadas

        df_original = df_original[['situacao_candidado',
                                   'recrutador',
                                   'cidade_candidato',
                                   'data_nascimento',
                                   'sexo',
                                   'estado_civil',
                                   'pcd',
                                   'remuneracao_candidato',
                                   'nivel_profissional_candidato',
                                   'nivel_academico_candidato',
                                   'nivel_ingles_candidato',
                                   'nivel_espanhol_candidato',
                                   'cursos_candidato',
                                   'cliente_vaga',
                                   'tipo_contratacao',
                                   'prioridade_vaga',
                                   'origem_vaga',
                                   'cidade_vaga',
                                   'nivel_profissional_vaga',
                                   'nivel_academico_vaga',
                                   'nivel_ingles_vaga',
                                   'nivel_espanhol_vaga',
                                   'areas_atuacao_vaga',
                                   'ultima_atualizacao']]

        df_original.drop_duplicates(inplace=True)  # Remove duplicatas

        # Convertendo as colunas para datetime, tratando erros
        df_original[['data_nascimento',
                     'ultima_atualizacao']] = df_original[['data_nascimento',
                                                           'ultima_atualizacao']].apply(lambda col: pd.to_datetime(col,
                                                                                                                   errors='coerce',
                                                                                                                   format='%d-%m-%Y'))

        # Extraindo apenas os números e convertendo para inteiro
        df_original['remuneracao_candidato'] = (
            df_original['remuneracao_candidato']
            # Remove tudo que não for número, vírgula, ponto ou hífen
            .str.replace(r'[^\d,.-]', '', regex=True)
            .str.replace(',', '.', regex=False)  # Substitui vírgula por ponto
            .str.extract(r'(-?\d+\.?\d*)')  # Captura o primeiro número válido
            .astype(float)  # Converte para float primeiro
            .fillna(0)  # Substitui NaN por 0 (opcional)
            .astype(int)  # Converte para inteiro
        )

        # Calculando a idade (diferenca entre anos)
        df_original['idade'] = df_original['ultima_atualizacao'].dt.year - \
            df_original['data_nascimento'].dt.year
        # Removendo as colunas 'data_nascimento' e 'ultima_atualizacao'
        df_original = df_original.drop(
            columns=[
                'data_nascimento',
                'ultima_atualizacao'])

        valores_positivos = [
            'Contratado pela Decision',
            'Aprovado',
            'Contratado como Hunting',
            'Proposta Aceita']
        df_original['situacao_candidado'] = df_original['situacao_candidado'].isin(
            valores_positivos).astype(int)

        df_original_X = df_original.drop(columns=["situacao_candidado"])
        df_original_Y = df_original["situacao_candidado"]

        # Remover NaN
        df_original_X = df_original_X.dropna()
        # Manter o mesmo índice de X
        df_original_Y = df_original_Y[df_original_X.index]

        le = LabelEncoder()

        # Lista das colunas a codificar
        colunas_categoricas = [
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

        folder_name = "files"

        # Verifica se a pasta existe e a cria se não existir
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        df_columns_selected = df_original_X[colunas_categoricas].copy()

        # Aplicando o LabelEncoder em cada coluna categórica
        for coluna in colunas_categoricas:
            df_columns_selected[coluna] = le.fit_transform(
                df_columns_selected[coluna])
            file_name = os.path.join(folder_name, f"LabelEncoder_{coluna}.pkl")

            if os.path.exists(file_name):
                os.remove(file_name)  # RECRIA

            joblib.dump(le, file_name)

        df_columns_selected, df_original_Y = SMOTE().fit_resample(
            df_columns_selected, df_original_Y)

        # Normalização/Escalonamento dos dados
        scaler = StandardScaler()

        X_normalized = scaler.fit_transform(df_columns_selected)

        folder_name = "files"
        file_name = os.path.join(folder_name, "scaler.pkl")

        # cria a pasta.
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        if os.path.exists(file_name):
            os.remove(file_name)  # RECRIA

        joblib.dump(scaler, file_name)

        # Identificando outliers
        z_scores = stats.zscore(X_normalized)
        outliers = (z_scores > 3).any(axis=1)

        # Remover outliers
        df_X_no_outliers = X_normalized[~outliers]
        df_Y_no_outliers = df_original_Y[~outliers]

        # 🔹 Dividindo em treino e teste

    except Exception as ex:
        # Se falhar o download/ carregamento de algum arquivo não é possível
        # seguir com o treinamento.
        print(ex)

    finally:
        return df_X_no_outliers, df_Y_no_outliers
