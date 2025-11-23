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
def get_things_to_do(destination: str, start_date: str, end_date: str) -> dict:
    """Get things to do in a destination city in given the start date and end date 
    to get the relevant months of travel and get things to do in those months.
    
    Args:
        destination: The city to explore
        start_date: The start date of the trip in YYYY-MM-DD format
        end_date: The end date of the trip in YYYY-MM-DD format"""
    months=[]
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    start_month_name = start_date_obj.strftime("%B")
    end_month_name = end_date_obj.strftime("%B")
    months.append(start_month_name)
    months.append(end_month_name)
    response = tavily_client.search(query=f"things to do in {destination} in {', '.join(months)}")
    return response

@tool
def get_foods_to_try(destination:str) -> dict:
    """Get popular foods to try in a destination city.
    
    Args:
        destination: The city to explore
    
    Returns:
        Dictionary with popular foods to try in the destination city
    """
    response = tavily_client.search(query=f"popular foods to try in {destination}")
    return response

def flight_finder_agent(from_city: str, to_city: str, depart_date: str, return_date: str = None):
    """ function to run a specialized agent to get flight options """
    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
    llm_with_tools = llm.bind_tools([search_flights])
    system_prompt = """You are a flight search specialist. Your job is to:
    1) Search for flights using the provided tool
    2) Summarize the flight options clearly with dates, prices and URLs
    3) Return only flight options in the form of a JSON array with airline names, departure times, arrival time, price, booking url and stops
    4) If no flights are found, respond with an empty json array []

    DO NOT INCLUDE ANY OTHER INFORMATION OR TEXT IN YOUR RESPONSE OTHER THAN THE JSON ARRAY 
    """
    if return_date:
        user_prompt = f"""Find round-trip flights from {from_city} to {to_city}.
        Departure: {depart_date}
        Return: {return_date}
        Provide flight options ONLY in JSON format with outbound and return flights.
        NO TEXT OTHER THAN THE JSON."""
    else:
        user_prompt = f"""Find one-way flights from {from_city} to {to_city}.
        Departure: {depart_date}
        Provide flight options ONLY in JSON format. NO TEXT OTHER THAN THE JSON."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = llm_with_tools.invoke(messages)
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        flight_results = search_flights.invoke(tool_call['args'])
        
        # Step 3: Send tool results back to agent for JSON formatting
        summary_prompt = f"""Based on these flight search results, format them as a clean JSON array.
        
        Flight data:
        {flight_results}
        
        Return ONLY the JSON array, no other text."""
        
        final_response = llm.invoke(summary_prompt)
        return final_response.content
    else:
        return response.content
    
def research_agent(destination: str, start_date: str, end_date: str):
    """ function to run a specialized agent to get things to do and foods to try """
    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
    llm_with_tools = llm.bind_tools([get_things_to_do, get_foods_to_try])
    system_prompt = """You are a travel research specialist. Your job is to:
    1) Use the provided tools to get things to do and popular foods to try in the destination city
    2) Summarize the information clearly with relevant details
    3) Return the information in a well-formatted list with bullet points in between these
    two tags: 
    <fun_activities> and </fun_activities>

    DO NOT INCLUDE ANY OTHER INFORMATION OR TEXT IN YOUR RESPONSE OTHER THAN THE LIST WITHIN THE TAGS 
    """
    user_prompt = f"""I am traveling to {destination} from {start_date} to {end_date}. 
    Please find me things to do and popular foods to try during my trip.
    Provide the information in a well-formatted list with bullet points within
    the tags 
    <fun_activities> and </fun_activities>. NO TEXT OTHER THAN THE LIST WITHIN THE TAGS."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Step 1: Send message to agent with tools
    response = llm_with_tools.invoke(messages)
    
    # Step 2: Check if tools were called and execute them
    if response.tool_calls:
        tool_results = []
        for tool_call in response.tool_calls:
            if tool_call['name'] == 'get_things_to_do':
                result = get_things_to_do.invoke(tool_call['args'])
                tool_results.append(f"Things to do: {result}")
            elif tool_call['name'] == 'get_foods_to_try':
                result = get_foods_to_try.invoke(tool_call['args'])
                tool_results.append(f"Foods to try: {result}")
        
        # Step 3: Send tool results back to agent for formatting
        summary_prompt = f"""Based on this research data, format it as a well-structured list with bullet points.
        
        Research data:
        {' '.join(tool_results)}
        
        Return ONLY the formatted list within <fun_activities> </fun_activities> tags, no other text."""
        
        final_response = llm.invoke(summary_prompt)
        return final_response.content
    else:
        return response.content

def manager_agent(from_city: str, to_city: str, depart_date: str, return_date: str):
    """Manager agent to coordinate flight and research agents."""

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