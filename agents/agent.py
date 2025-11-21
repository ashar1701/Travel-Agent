import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from tavily import TavilyClient
from datetime import datetime

load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_SEARCH_API_KEY"))

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
    if return_date is None:
        response = tavily_client.search(query=f"flights from {origin} to {destination} on {departure_date}")
        return response

    response = tavily_client.search(query=f"flights from {origin} to {destination} on {departure_date} and return on {return_date}")
    return response

@tool
def get_month_from_dates(start_date: str, end_date: str) -> str:
    """Extract the matching month from the provided start and end dates to make it easier to search for things to do"""
    months=[]
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    start_month_name = start_date_obj.strftime("%B")
    end_month_name = end_date_obj.strftime("%B")
    months.append(start_month_name, end_month_name)

    if start_month_name == end_month_name:
        return months[0]
    else:
        return months
    
@tool
def get_things_to_do(destination: str, months) -> dict:
    """Get things to do in a destination city in that month that is decoded.
    
    Args:
        destination: The city to explore
        months: The month or months to explore activities in"""
    response = tavily_client.search(query=f"things to do in {destination} in {', '.join(months)}")
    return response


# def main():
#     """Main function to run the travel agent for flight search."""
    
#     # Initialize the Gemini model
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash-lite",
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         temperature=0.7
#     )
#     llm_with_tools = llm.bind_tools([search_flights])
    
#     # Create the initial user prompt
#     user_query = """I want to go on a vacation trip from New York to London. 
#     I am looking to depart on 2025-11-22 and return on 2025-11-28. 
#     Can you search for flights and provide me with a summary of available options including URLs and prices?"""
#     response = llm_with_tools.invoke(user_query)
#     if response.tool_calls:
#         print(" Flight search tool called by agent\n")
#         tool_call = response.tool_calls[0]
#         print(f"Tool: {tool_call['name']}")
#         print(f"Arguments: {tool_call['args']}\n")
        
#         # Call the search_flights function directly
#         flight_results = search_flights.invoke(tool_call['args'])
        
#         # Step 3: Send the tool results back to the model for summarization
#         print(" Processing flight data...\n")
        
#         summary_prompt = f"""Based on the following flight search results, please provide a clear, 
#         well-formatted summary of the available flight options. Include:
#         - Airline names if available
#         - Prices
#         - Booking URLs
#         - Any other relevant information
        
#         Format the response in an easy-to-read list format with bullet points.
        
#         Flight Search Results:
#         {flight_results}
#         """
        
#         summary_response = llm.invoke(summary_prompt)
#         print("  FLIGHT SEARCH SUMMARY")
#         print(summary_response.content)
#     else:
#         print("Response from Gemini:")
#         print(response.content)

# if __name__ == "__main__":
#     main()