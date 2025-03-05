import json
import uvicorn
from fastapi import FastAPI
from src.web import creature 
from src.data.schemas import CreatureBase
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer

origins = [
    "http://localhost:8003",
    # "*", //allow all
]

app = FastAPI(swagger_ui_parameters={"displayModelsExpandDepth": -1})
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(creature.router, tags=["Creature"])

def json_serializer(data):
    return json.dumps(data).encode('utf-8')
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         api_version=(0,11,5),
                         value_serializer = json_serializer)
@app.post("/publish/{topic}")
def publish(topic: str, data: CreatureBase):
    message = json.loads(data.model_dump_json())
    producer.send(topic,message)
    return {"status": "Message published successfully", "topic": topic, "data": message}

if __name__ == "__main__":
    # import uvicorn
    uvicorn.run("creature:app", reload=True, host="0.0.0.0", port=8001)