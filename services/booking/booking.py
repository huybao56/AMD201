import json
import uvicorn
from fastapi import FastAPI
from src.model.booking import booking_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8003",
    # "*", # allow all
]

app = FastAPI(swagger_ui_parameters={"displayModelsExpandDepth": -1})
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(booking_router, tags=["Booking"])

if __name__ == "__main__":
    uvicorn.run("booking:app", reload=True, host="0.0.0.0", port=8003)