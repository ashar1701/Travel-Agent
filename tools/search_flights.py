from datetime import datetime
import os
from dotenv import load_dotenv
from tavily import TavilyClient

def search_flights(origin, destination, departure_date=None, return_date=None):
    if departure_date is None:
        departure_date = datetime.now().strftime("%Y-%m-%d")
    client = TavilyClient(api_key=os.getenv("TAVILY_SEARCH_API_KEY"))
    if return_date is None:
        response = client.search(query=f"flights from {origin} to {destination} on {departure_date}")
        return response

    response = client.search(query=f"flights from {origin} to {destination} on {departure_date} and return on {return_date}")
    return response


def main():
    load_dotenv()
    origin = "New York"
    destination = "London"
    departure_date = "2025-12-01"
    return_date = "2025-12-08"
    response = search_flights(origin, destination, departure_date, return_date)
    print(response)




