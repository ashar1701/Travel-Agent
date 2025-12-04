from datetime import date
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.agent import manager_agent 

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
    """Delegate trip planning to the multi-agent workflow and expose the result."""
    try:
        plan_text = manager_agent(
            trip_request.origin,
            trip_request.destination,
            trip_request.departure_date.isoformat(),
            trip_request.return_date.isoformat() if trip_request.return_date else None,
        )
    except Exception as exc:  # pragma: no cover - surfaces upstream failures
        raise HTTPException(status_code=500, detail="Unable to generate travel plan") from exc
    
    print("Generated travel plan:", plan_text)

    return {"plan": plan_text}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)