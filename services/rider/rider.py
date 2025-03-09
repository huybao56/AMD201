import json
import uvicorn
from fastapi import FastAPI
from src.model.rider import rider_router
from src.model.rider import RiderProducer
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer
from kafka import KafkaConsumer

origins = [
    "http://localhost:8000",
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

app.include_router(rider_router, tags=["Rider"])
# Kafka Producer
def json_serializer(data):
    return json.dumps(data).encode('utf-8')
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        api_version=(0,11,5),
                        value_serializer = json_serializer)
@app.post("/accept/",summary="Accept Booking", tags=["Producer"])
def publish(topic: str,data: RiderProducer):
    message = json.loads(data.model_dump_json())
    producer.send(topic,message)
    return {"status": "Accepted successfully","Rider Information": message}


# Kafka Consumer
consumer = KafkaConsumer("Booking",bootstrap_servers='localhost:9092',
                            group_id='my_consumer_group',        
                            auto_offset_reset='earliest',        # Read from beginning if no offset found
                            enable_auto_commit=True,              # Enable auto-commit (optional)
                            api_version=(0,11,5),
                            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe(pattern=".*")  # Matches all topics
@app.get("/search/", summary="Searching Passenger", tags=["Consumer"])
def consume():
    for message in consumer:  # Get the latest message
        passenger_data = message.value
        return {
            "status": "Found Out!",
            "Passenger": {
                "name": passenger_data.get("name"),
                "phone_number": passenger_data.get("phone_number"),
                "pickup_location": passenger_data.get("pickup_location"),
                "dropoff_location": passenger_data.get("dropoff_location"),
                "payment_method": passenger_data.get("payment_method"),
            }
        }
    
@app.get("/Notifications_Rating/", summary="Rider Rating", tags=["Consumer"])
def consume():
    for message in consumer:  # Get the latest message
        passenger_data = message.value
        return {
            "status": "You have received your ratings",
            "Passenger": {
                "name": passenger_data.get("name"),
                "rating": passenger_data.get("rating")
            }
        }
    
if __name__ == "__main__":
    uvicorn.run("rider:app", reload=True, host="0.0.0.0", port=8002)