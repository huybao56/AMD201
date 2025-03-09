from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # Thêm import này
import httpx
from sqlalchemy.orm import Session
from src.model.user import user_router
from src.model.rider import rider_router
from src.model.booking import booking_router

services = {
    "user": "http://localhost:8001",
    "rider": "http://localhost:8002",
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(rider_router, prefix="/rider", tags=["Rider"])
app.include_router(booking_router, prefix="/booking", tags=["Booking"])

async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    async with httpx.AsyncClient() as client:
        url = f"{service_url}{path}"
        response = await client.request(method, url, json=body, headers=headers)
        return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=8000)