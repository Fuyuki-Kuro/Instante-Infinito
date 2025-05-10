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

def obter_todas_entradas(user_names: dict):
    """ Retorna todas as entradas de todos os usuários com autor. """
    todas = []
    for filename in os.listdir(DIARIO_PATH):
        if filename.endswith(".json"):
            user_id = filename.replace(".json", "")
            nome = user_names.get(user_id, "Desconhecido")
            caminho = os.path.join(DIARIO_PATH, filename)
            with open(caminho, "r", encoding="utf-8") as f:
                entradas = json.load(f)
                for entrada in entradas:
                    entrada["author"] = nome
                    entrada["user_id"] = user_id
                    todas.append(entrada)
    # Ordena por data se possível
    try:
        todas.sort(key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y %H:%M"), reverse=True)
    except Exception:
        pass
    return todas
