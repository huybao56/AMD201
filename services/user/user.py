import json
import uvicorn
from fastapi import FastAPI
from src.model.user import user_router
from src.model.user import UserProducer, UserProducerRating
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer
from kafka import KafkaConsumer

origins = [
    "http://localhost:8000"
]

app = FastAPI(swagger_ui_parameters={"displayModelsExpandDepth": -1})
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, tags=["User"])

# Kafka Producer
def json_serializer(data):
    return json.dumps(data).encode('utf-8')
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        api_version=(0,11,5),
                        value_serializer = json_serializer)
@app.post("/booking/",summary="Booking Rider", tags=["Producer"])
def publish(topic: str,data: UserProducer):
    message = json.loads(data.model_dump_json())
    producer.send(topic,message)
    return {"status": "Booking successfully","User's Booking": message}

@app.post("/rating/",summary="Rating Rider", tags=["Producer"])
def publish(topic: str,data: UserProducerRating):
    message = json.loads(data.model_dump_json())
    producer.send(topic,message)
    return {"status": "Rating successfully","User's Rating": message}


# Kafka Consumer
consumer = KafkaConsumer("accepted",bootstrap_servers='localhost:9092',
                            group_id='my_consumer_group_user',        
                            auto_offset_reset='earliest',        # Read from beginning if no offset found
                            enable_auto_commit=True,              # Enable auto-commit (optional)
                            api_version=(0,11,5),
                            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe(pattern=".*")  # Matches all topics
@app.get("/acceptance/", summary="Rider Distance", tags=["Consumer"])
def consume():
    for message in consumer:
        rider_data = message.value
        return {"status": "Your Rider is coming...", 
            "Rider":{
                "name": rider_data.get("name"),
                "phone_number": rider_data.get("phone_number"),
                "license_plate" : rider_data.get("license_plate"),
                "distance_from_rider": rider_data.get("distance_from_rider"),
                "price": rider_data.get("price"),
            }}  
        



if __name__ == "__main__":
    uvicorn.run("user:app", reload=True, host="0.0.0.0", port=8001)