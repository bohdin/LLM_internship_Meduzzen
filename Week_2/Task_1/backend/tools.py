import json
import random

import wikipedia
from langchain.tools import Tool


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


def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for a summary of the given query.

    Args:
        query (str): Key words for searching.

    Returns:
        str: A summary related to the query.
    """
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.PageError:
        return "Page not found"


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
        func=search_wikipedia,
        name="search_wikipedia",
        description="Search information by given query.",
    ),
    Tool.from_function(
        func=get_weather,
        name="get_weather",
        description="Get current temperature for a given location.",
    ),
]
