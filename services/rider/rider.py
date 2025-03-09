import json
import uvicorn
from fastapi import FastAPI
from src.web import rider
from src.data.init import create_tables
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer # type: ignore

origins = [
    "http://localhost:8002",
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

app.include_router(rider.router, tags=["Rider"])

# Kafka
consumer = KafkaConsumer("my_topic", bootstrap_servers='localhost:9092',
                         api_version=(0,11,5),
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
@app.get("/consume")
def consume():
    messages = []
    for message in consumer:
        messages.append(message.value)
        if len(messages) >= 3:
            break
    return {"status": "Received successfully", "data": messages}  


if __name__ == "__main__":
    uvicorn.run("rider:app", reload=True, host="0.0.0.0", port=8002)