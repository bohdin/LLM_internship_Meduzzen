import json
import os
import random

from langchain.tools import Tool

from vector_store import VectorStore

vector_store = VectorStore()


def calculate_area_rectangle(json_input: str) -> float:
    """
    Calculate the area of a rectangle from a JSON string.

    Args:
        json_input (str): A JSON string with keys "height" and "width".

    Returns:
        float: The calculated area of the rectangle.
    """
    data = json.loads(json_input)
    height = float(data.get("height"))
    width = float(data.get("width"))

    return height * width


def search_info(query: str) -> str:
    """
    Perform a retrieval-augmented search using vectorstore.

    Args:
        query (str): User's search query.

    Returns:
        str: Retrieved information or empty string if no relevant info found.
    """
    return vector_store.search(query, api_key=os.getenv("OPENAI_API_KEY"))


def get_weather(location: str) -> float:
    """
    Returns fake temperature for the given location.

    Args:
        location (str): The name of the city and country.

    Returns:
        float: A random temperature between -20.0 and 20.0.
    """
    return round(random.uniform(-20, 20), 1)


tools = [
    Tool.from_function(
        func=calculate_area_rectangle,
        name="calculate_area_rectangle",
        description="Calculating an area for rectangle by given height and width. Input: JSON string with keys 'height' and 'width'.",
    ),
    Tool.from_function(
        func=search_info,
        name="search_info",
        description=(
            "You must always use this tool FIRST to answer any user question, even if you know answer "
            "whether the information is in the documents or not. "
            "This includes any question, general or specific, technical or non-technical. "
            "Only if the tool returns no useful information, answer from your own knowledge."
        ),
    ),
    Tool.from_function(
        func=get_weather,
        name="get_weather",
        description="Get current temperature for a given location.",
    ),
]
