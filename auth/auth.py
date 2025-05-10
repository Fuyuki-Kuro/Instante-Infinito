import jwt
import datetime
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
load_dotenv()


# Chave secreta — mantenha isso em segredo e fora do código-fonte se possível
SECRET_KEY = os.getenv("SECRET_KEY")

def gerar_token(user_id: int):
    payload = {
        "sub": str(user_id),  # ou "user_id"
        "exp": datetime.now(timezone.utc) + timedelta(days=3650)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
