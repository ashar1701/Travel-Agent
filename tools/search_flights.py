from datetime import datetime
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool

@tool
def search_flights(origin: str, destination: str, departure_date: str = None, return_date: str = None) -> dict:
    """Search for flights between two cities with departure and optional return dates.
    
    Args:
        origin: The departure city
        destination: The arrival city
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format (optional)
    
    Returns:
        Dictionary with flight search results including URLs and prices
    """
    if departure_date is None:
        departure_date = datetime.now().strftime("%Y-%m-%d")
    
    load_dotenv()
    client = TavilyClient(api_key=os.getenv("TAVILY_SEARCH_API_KEY"))
    if return_date is None:
        response = client.search(query=f"flights from {origin} to {destination} on {departure_date}")
        return response

    response = client.search(query=f"flights from {origin} to {destination} on {departure_date} and return on {return_date}")
    return response




