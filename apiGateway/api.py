from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
# from src.model import explorer, creature #Init db
# from src.data.init import create_tables
from fastapi.middleware.cors import CORSMiddleware

services = {
    # "creature": "http://localhost:8001",
    # "explorer": "http://localhost:8002",
}


origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    async with httpx.AsyncClient() as client:
        url = f"{service_url}{path}"
        # print(f"{body}")
        response = await client.request (method, url, json=body, headers=headers)
        return response

@app.api_route("/gateway/{service}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["ApiGateway"])
async def gateway (service: str, request: Request, parameter: Optional [str] = ""):
    if service not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service_url = services[service]
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None
    
    response = await forward_request(service_url, request.method, f"/{service}/{parameter}", body, None)

    return JSONResponse(status_code=response.status_code, content=response.json())

if __name__ == "__main__":
    # create_tables()
    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=8000)