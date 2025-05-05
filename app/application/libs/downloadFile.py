import os
import requests
from tqdm.auto import tqdm


def create_dir(folderName: str):
    print("Cliendo pasta files")
    os.makedirs(folderName)


def download_file(url, destination, folderName: str = "files"):
    """Baixa um arquivo da URL fornecida com uma barra de progresso."""

    if not os.path.exists("files"):
        create_dir(folderName)

    try:
        result = requests.get(url, stream=True)
        result.raise_for_status()
        total_size_in_bytes = int(result.headers.get('content-length', 0))
        # block_size = 1024  # 1 Kibibyte

        with tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=destination, unit_divisor=1024) as progress_bar:

            with open("files/" + destination, 'wb') as arquivo_destino:
                for chunk in result.iter_content(chunk_size=8192):
                    arquivo_destino.write(chunk)
                    progress_bar.update(len(chunk))

            print(f"Arquivo baixado com sucesso como: {destination}")

        return True

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return False

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
