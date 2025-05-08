from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from trigger_state import state
import datetime
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve arquivos estáticos da pasta 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Pega a data de quando se conheceram
    date_met = datetime.datetime.fromisoformat(state["date_met"])

    # Passa a data para o template
    return templates.TemplateResponse("index.html", {"request": request, "date_met": date_met})