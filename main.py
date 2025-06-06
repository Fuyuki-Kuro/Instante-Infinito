import os
import logging
import jwt
from jwt.exceptions import PyJWTError
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from diario.diario_storage import adicionar_entrada, obter_entradas, obter_todas_entradas

# Carrega variáveis de ambiente
load_dotenv()

USER_NAMES = {
    os.getenv("ID_HE"): "Leonardo",
    os.getenv("ID_SHE"): "Angélica",
}

# Configuração de logs
logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Inicializa FastAPI
app = FastAPI()
# Monta arquivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Chave secreta para JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if isinstance(SECRET_KEY, str):
    SECRET_KEY = SECRET_KEY.encode("utf-8")

DATE_MET = os.getenv("DATE_MET")  # já vem como string

# Função de verificação de token JWT
def verify_token(token: str, request: Request = None):
    if not token:
        logging.error("Token ausente no request")
        return templates.TemplateResponse("unauthorized.html", {"request": request}, status_code=403)
    try:
        # Converter token para bytes se necessário
        token_bytes = token.encode("utf-8") if isinstance(token, str) else token
        payload = jwt.decode(token_bytes, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub") or payload.get("user_id")
        if not user_id:
            logging.error("Token sem campo sub/user_id: %s", token)
            return templates.TemplateResponse("unauthorized.html", {"request": request}, status_code=403)
        return str(user_id)
    except PyJWTError as e:
        logging.error(f"Token inválido ao decodificar: {e}")
        return templates.TemplateResponse("unauthorized.html", {"request": request}, status_code=403)

# Rota principal
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    token = request.query_params.get("token")
    user_id = verify_token(token, request)
    if isinstance(user_id, str):
        return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id, "date_met": DATE_MET})
    return user_id  # resposta de unauthorized

# Rota do diário
@app.get("/diario", response_class=HTMLResponse)
async def diario(request: Request):
    token   = request.query_params.get("token")
    uid     = verify_token(token)
    entries = obter_todas_entradas(USER_NAMES)
    name = USER_NAMES.get(uid)
    return templates.TemplateResponse("diario.html", {
        "request": request,
        "entradas": entries,
        "token": token,
        "name": name
    })

@app.post("/diario", response_class=HTMLResponse)
async def escrever_entrada(request: Request, mensagem: str = Form(...)):
    token = request.query_params.get("token")
    uid   = verify_token(token)
    adicionar_entrada(uid, mensagem)
    name = USER_NAMES.get(uid)
    # Importa dinamicamente para evitar dependência circular
    from bot import notify_new_diary_entry
    notify_new_diary_entry(uid, mensagem)
    entries = obter_todas_entradas(USER_NAMES)
    return templates.TemplateResponse("diario.html", {
        "request": request,
        "entradas": entries,
        "token": token,
        "name": name
    })

# Endpoint dummy para validação WebApp
@app.post("/validate_webapp")
async def validate_webapp():
    return {"valid": True}

# Página de acesso negado
@app.get("/unauthorized")
async def unauthorized(request: Request):
    return templates.TemplateResponse("unauthorized.html", {"request": request}, status_code=403)

def main():
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=9000)