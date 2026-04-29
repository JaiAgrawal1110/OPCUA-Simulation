from pymongo import MongoClient
import random
import time
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["CNC_DATA"]
collection = db["Machine_status"]

while True:
    data = {
        "spindle_speed": random.randint(1000, 3000),
        "temperature": round(random.uniform(30.0, 70.0), 2),
        "status": random.choice(["Running", "Idle", "Error"]),
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(data)
    print("Inserted:", data)
    time.sleep(2)
