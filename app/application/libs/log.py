from datetime import datetime
import os, json


def salvar_log_json(info, result):

    # Define nome do arquivo com base na data atual
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"log_predict_{date_str}.json")

    # Monta o log
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entrada": info,
        "saida": result
    }

    # Lê logs anteriores (se existirem)
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log)

    # Salva
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)
