import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

load_dotenv()

def tvly_agent():
    client = TavilyClient(api_key=os.getenv("TAVILY_SEARCH_API_KEY"))
    response = client.search(query="5 fun facts about switzerland")
    return response

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)
response = tvly_agent()
print("Response from Tavily:", response)
# Create a basic prompt
prompt = f"""Look at the following response ${response} Tell me one fun fact about switzerland from this."""

# Invoke the model and get the response
response = llm.invoke(prompt)

# Print the response
print("Response from Gemini:")
print(response.content)