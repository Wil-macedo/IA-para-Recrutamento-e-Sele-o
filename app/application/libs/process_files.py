
import os
import json
import pandas as pd
from typing import Union
from .downloadFile import download_file


class Files:

    S3_URLBASE = "https://tc-f5-files.s3.us-east-1.amazonaws.com/"

    def __init__(self, file_name: str):

        self.file_name = file_name

        self.path = os.path.join(os.getcwd(), "files", self.file_name)
        self.url_s3 = self.S3_URLBASE + self.file_name

        self.check_file()

    def download(self):
        if download_file(self.url_s3, self.file_name):
            print(f"{self.file_name} - DOWNLOAD OK")
        else:
            raise (f"FALHA NO DOWNLOAD DO ARQUIVO {self.file_name} NO S3")

    def check_file(self):

        _folder = "files"
        if not os.path.exists(_folder):
            os.makedirs(_folder)
            print(f"CRIANDO DIRETÓRIO {_folder}")

        if os.path.exists(self.path):
            print(f"{self.path} - OK")
        else:
            print(f"{self.file_name} - DOWNLOADING......... ")
            self.download()

    def __repr__(self):
        return f"PROCESSING {self.file_name}"


def processar_json(file_path: str, key: str) -> pd.DataFrame:

    with open(file_path, 'r', encoding='utf-8') as f:
        data: dict = json.load(f)

    _records: list = []
    for id_profissional, dados in data.items():
        registro = {key: id_profissional}  # Adiciona o ID como coluna

        # Percorre todas as seções do JSON
        for secao, _values in dados.items():
            if isinstance(
                    _values,
                    dict):  # Se a seção tiver subitens, adiciona normalmente
                registro.update(_values)
            else:  # Se for um valor único (ex: cv_pt, cv_en, cargo_atual vazio)
                registro[secao] = _values

        _records.append(registro)

    return pd.DataFrame(_records)


def processar_json_para_dataframe(json_data: Union[dict, str]) -> pd.DataFrame:
    _data: list = []

    if isinstance(json_data, dict):
        # Não precisa de leitura.
        pass

    elif isinstance(json_data, str):

        with open(json_data, "r", encoding="utf-8") as file:
            json_data = json.load(file)

    else:
        raise ("TIPO DE DADO INCOMPATÍVEL - processar_json_para_dataframe()")

    for id_vaga, vaga_info in json_data.items():
        vaga_info: dict

        titulo = vaga_info.get("titulo", "")
        modalidade = vaga_info.get("modalidade", "")

        # Se houver uma lista dentro do JSON, criamos múltiplas linhas
        if "prospects" in vaga_info:
            for prospect in vaga_info["prospects"]:
                linha = {
                    "id_vaga": id_vaga,
                    "titulo": titulo,
                    "modalidade": modalidade}
                # Adiciona os dados de prospects como colunas
                linha.update(prospect)
                _data.append(linha)
        else:
            _data.append({"id_vaga": id_vaga, "titulo": titulo,
                         "modalidade": modalidade})

    return pd.DataFrame(_data)