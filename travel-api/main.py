from datetime import date
import uvicorn 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


class TripRequest(BaseModel):
    origin: str
    destination: str
    departure_date: date
    return_date: date | None = None

@app.post("/plan-trip")
def plan_trip(trip_request: TripRequest):
    # Implement your trip planning logic here
    return {
        "itinerary": [
            {"day": 1, "summary": f"fly from {trip_request.origin} to {trip_request.destination}"},
            {"day": 2, "summary": f"explore {trip_request.destination}"}
        ]
    }

app = FastAPI()

origins = ["http://localhost:5173/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)