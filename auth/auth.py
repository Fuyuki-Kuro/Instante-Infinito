import jwt
import datetime
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
load_dotenv()


# Chave secreta — mantenha isso em segredo e fora do código-fonte se possível
SECRET_KEY = os.getenv("SECRET_KEY")
if isinstance(SECRET_KEY, str):
    SECRET_KEY = SECRET_KEY.encode("utf-8")

def gerar_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=3650)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    # Converter para string se for bytes
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token
