from fastapi import FastAPI, Form, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from trigger_state import state
import datetime
from fastapi import Request
import uvicorn
import os
from dotenv import load_dotenv
from trigger_state import state
from auth import auth
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException
import jwt
from jwt.exceptions import PyJWTError
from diario.diario_storage import adicionar_entrada, obter_entradas
load_dotenv()

import logging

# Configura o logger
logging.basicConfig(
    filename="app.log",          # Nome do arquivo de log
    level=logging.ERROR,         # Nível mínimo de log
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI()
templates = Jinja2Templates(directory="templates")
SECRET_KEY = os.getenv("SECRET_KEY")
if isinstance(SECRET_KEY, str):
    SECRET_KEY = SECRET_KEY.encode("utf-8")

# Serve arquivos estáticos da pasta 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

def verify_token(token: str = Query(...), request: Request = None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=403, detail="Invalid token payload")
        return str(user_id)
    except PyJWTError as e:
        print("Token inválido:", e)
        raise HTTPException(status_code=403, detail="Invalid token")
    
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    token = request.cookies.get("token")
    user_id = verify_token(token, request)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_id": user_id
    })

@app.get("/diario", response_class=HTMLResponse)
async def diario(request: Request):
    token = request.cookies.get("token")
    user_id = verify_token(token, request)
    entradas = obter_entradas(user_id)  # Você deve implementar isso
    return templates.TemplateResponse("diario.html", {
        "request": request,
        "entradas": entradas
    })

@app.post("/diario", response_class=HTMLResponse)
async def escrever_entrada(
    request: Request,
    mensagem: str = Form(...),
):
    token = request.cookies.get("token")
    user_id = verify_token(token, request)
    # Adiciona a nova entrada ao diário
    adicionar_entrada(user_id, mensagem)

    # Obtém todas as entradas do diário do usuário
    entradas = obter_entradas(user_id)

    # Retorna a página com as entradas atualizadas
    return templates.TemplateResponse("diario.html", {
        "request": request,
        "entradas": entradas
    })

@app.post("/validate_webapp")
async def validate_webapp():
    # apenas para evitar erro 404 por enquanto
    return {"status": "ok"}

@app.get("/unauthorized")
async def unauthorized(request: Request):
    return templates.TemplateResponse("unauthorized.html", {"request": request}, status_code=403)

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)