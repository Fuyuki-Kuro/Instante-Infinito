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
from diario.diario_storage import adicionar_entrada, obter_entradas

# Carrega variáveis de ambiente
load_dotenv()

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
        return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id})
    return user_id  # resposta de unauthorized

# Rota do diário
@app.get("/diario", response_class=HTMLResponse)
async def diario(request: Request):
    token = request.query_params.get("token")
    user_id = verify_token(token, request)
    if not isinstance(user_id, str):
        return user_id
    entradas = obter_entradas(user_id)
    return templates.TemplateResponse("diario.html", {"request": request, "entradas": entradas})

@app.post("/diario", response_class=HTMLResponse)
async def escrever_entrada(request: Request, mensagem: str = Form(...)):
    token = request.query_params.get("token")
    user_id = verify_token(token, request)
    if not isinstance(user_id, str):
        return user_id
    adicionar_entrada(user_id, mensagem)
    entradas = obter_entradas(user_id)
    return templates.TemplateResponse("diario.html", {"request": request, "entradas": entradas})

# Endpoint dummy para validação WebApp
@app.post("/validate_webapp")
async def validate_webapp():
    return {"status": "ok"}

# Página de acesso negado
@app.get("/unauthorized")
async def unauthorized(request: Request):
    return templates.TemplateResponse("unauthorized.html", {"request": request}, status_code=403)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 9000)), reload=True)
