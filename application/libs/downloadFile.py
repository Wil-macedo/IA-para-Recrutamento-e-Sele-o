import os
import requests
import tqdm

def download_file(url, destination):
    """Baixa um arquivo da URL fornecida com uma barra de progresso."""
    
    if not os.path.exists("files"):
        print("Cliendo pasta files")
        os.makedirs("files")
    
    try:
        resposta = requests.get(url, stream=True)
        resposta.raise_for_status()
        total_size_in_bytes = int(resposta.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        with tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=destination) as progress_bar:
            with open("files/" + destination, 'wb') as arquivo_destino:
                for chunk in resposta.iter_content(chunk_size=block_size):
                    arquivo_destino.write(chunk)
                    progress_bar.update(len(chunk))

        print(f"\nArquivo baixado com sucesso como: {destination}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")