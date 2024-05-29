from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from main import main

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")


class ConvertCodeRequest(BaseModel):
    code: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/compile")
async def compile_code(code_request: ConvertCodeRequest):
    try:
        output_code = main(code_request.code)
        return {"output_code": output_code, "error": None}
    except Exception as e:
        return {"output_code": "", "error": str(e)}
