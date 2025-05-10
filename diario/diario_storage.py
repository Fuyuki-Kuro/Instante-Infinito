import os
import json
from datetime import datetime

DIARIO_PATH = "diario/entradas"

# Garante que o diretório exista
os.makedirs(DIARIO_PATH, exist_ok=True)

def _caminho_usuario(user_id):
    return os.path.join(DIARIO_PATH, f"{user_id}.json")

def obter_entradas(user_id):
    caminho = _caminho_usuario(user_id)
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def adicionar_entrada(user_id, mensagem):
    entradas = obter_entradas(user_id)
    nova_entrada = {
        "mensagem": mensagem,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    entradas.append(nova_entrada)
    with open(_caminho_usuario(user_id), "w", encoding="utf-8") as f:
        json.dump(entradas, f, ensure_ascii=False, indent=2)
