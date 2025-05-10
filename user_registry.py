# user_registry.py
import os
import json

USERS_FILE = "users.json"

# Carrega ou inicializa o registro de usuários que deram /start
def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Salva o registro de usuários
def _save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# Adiciona ou atualiza um usuário (id e nome)
def add_user(user_id: int, first_name: str):
    users = _load_users()
    users[str(user_id)] = first_name
    _save_users(users)

# Retorna todos os usuários registrados como {id: name}
def get_all_users() -> dict:
    return _load_users()


# bot_notifications.py
from telebot import TeleBot
from user_registry import get_all_users
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = TeleBot(TOKEN)

# Notifica todos os usuários sobre uma nova entrada
def notify_new_diary_entry(author_id: int, message_text: str):
    users = get_all_users()
    author_name = users.get(str(author_id), "Alguém")
    text = f"💌 *Nova entrada no diário de {author_name}* 💌\n\n{message_text}"
    for uid in users.keys():
        try:
            bot.send_message(int(uid), text, parse_mode="Markdown")
        except Exception as e:
            print(f"Erro ao notificar {uid}: {e}")
