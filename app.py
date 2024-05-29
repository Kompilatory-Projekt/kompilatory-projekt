from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from main import convert_code

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from pydantic import BaseModel
class ConvertCodeRequest(BaseModel):
    code: str

@app.post("/compile", response_class=HTMLResponse)
async def compile_code(code_request: ConvertCodeRequest):

    output_code = convert_code(code_request)
    
    return templates.TemplateResponse("index.html", {"request": request, "output_code": output_code})