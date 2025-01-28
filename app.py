from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent , AgentType
import streamlit as st

load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


@tool
def calculator(expression: str) -> float:
    """
    Evaluates a mathematical expression safely.

    Parameters:
        expression (str): A string representing a mathematical expression.

    Returns:
        float: The result of the evaluated expression.

    Example:
        calculator("3 + 5 * 2") -> 13.0
        calculator("(10 / 2) ** 2") -> 25.0
    """
    import math

    # Define allowed functions and constants
    allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    allowed_names.update({"abs": abs, "round": round})

    # Evaluate the expression
    try:
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid mathematical expression: {e}")

import requests

newsapi = "421f8b3ead224d6a92239568c87f0058"


@tool
def news(api_key: str, query: str = None, language: str = 'en', page_size: int = 10):
    """
    Fetch the latest news articles using a news API.

    Parameters:
        api_key (str): Your API key for the news service.
        query (str, optional): A specific topic to search for news articles. Defaults to None for general news.
        language (str, optional): Language code for the news (e.g., 'en' for English). Defaults to 'en'.
        page_size (int, optional): Number of articles to retrieve. Defaults to 10.

    Returns:
        list: A list of dictionaries containing news articles, and their titles.
    """
    r = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
    )  # Aligned with the function definition
    if r.status_code == 200:
        # Parse the JSON response
        data = r.json()

        # Extract the articles
        articles = data.get("articles", [])

        # Print the headlines
        for article in articles:
            print(article["title"])

tools = [calculator,news]

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)

agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

st.title("Gemini Tool Calling")
st.write("Welcome To My APP")
user_input = st.text_input("Enter Your Prompt")


if st.button("Submit"):
    response = agent.invoke(user_input)
    st.write(response["output"]) 