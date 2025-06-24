from pydantic import BaseModel, Field
from langchain.tools import Tool
from langchain_core.tools import tool
import random
import json

import wikipedia

class RectangleInput(BaseModel):
    height: float = Field(..., description="Height of the rectangle")
    width: float = Field(..., description="Width of the rectangle")

def calculate_area_rectangle(json_input: str) -> float:
    """
    Calculate the area of a rectangle.

    Args:
        height (float): Height of the rectangle.
        width (float): Width of the rectangle.

    Returns:
        float: An area of rectangle.
    """
    data = json.loads(json_input)
    height = data.get("height")
    width = data.get("width")

    if height is None or width is None:
        return "Error: please provide 'height' and 'width' fields."

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
        return wikipedia.summary(query, sentences = 2)
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
        description="Search information by given query."
    ),
    Tool.from_function(
        func=get_weather,
        name="get_weather",
        description="Get current temperature for a given location."
    ),
]