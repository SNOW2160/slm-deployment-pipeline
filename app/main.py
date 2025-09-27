from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
from .inference import get_adapter
from .config import API_KEY

app = FastAPI(title="SLM Starter API")
adapter = get_adapter()

class GenReq(BaseModel):
    prompt: str
    max_tokens: int = 64
    temperature: float = 0.7

def check_auth(request: Request):
    key = request.headers.get("x-api-key") or request.query_params.get("api_key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/generate")
async def generate(req: GenReq, request: Request):
    check_auth(request)
    start = time.time()
    res = adapter.generate(req.prompt, max_tokens=req.max_tokens, temperature=req.temperature)
    elapsed = time.time() - start
    return JSONResponse({"generated_text": res.text, "latency_seconds": elapsed})

@app.get("/health")
async def health():
    return {"status": "ok"}
