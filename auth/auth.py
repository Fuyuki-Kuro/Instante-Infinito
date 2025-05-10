import jwt
import datetime
import os
from dotenv import load_dotenv
from datetime import UTC
load_dotenv()


# Chave secreta — mantenha isso em segredo e fora do código-fonte se possível
SECRET_KEY = os.getenv("SECRET_KEY")

def gerar_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365 *10)  # expira em 7 dias
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# IDs autorizados
user_ids = [7023797414, 1913979924]  # exemplo: você e ela

# Gerando os tokens para cada ID
for uid in user_ids:
    token = gerar_token(uid)
    print(f"Token para ID {uid}:\n{token}\n")
