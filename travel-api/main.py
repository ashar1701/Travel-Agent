from datetime import date
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    origin: str
    destination: str
    departure_date: date
    return_date: date | None = None

@app.post("/plan-trip")
def plan_trip(trip_request: TripRequest):
    """Return a placeholder itinerary until AI integration is ready."""
    print(f"Received trip request: {trip_request}")
    return {
        "itinerary": [
            {
                "day": 1,
                "summary": f"Fly from {trip_request.origin} to {trip_request.destination}",
            },
            {"day": 2, "summary": f"Explore {trip_request.destination}"},
        ]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)