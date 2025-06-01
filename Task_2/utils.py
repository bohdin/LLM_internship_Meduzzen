import json
import os
import random
from datetime import datetime, timezone

import wikipedia


def call_function(name: str, args: dict[str, str | float]) -> str | float:
    """
    Calls the appropriate function based on the given function name and arguments

    Args:
        name (str): The name of the function to call
        args (dict[str, str | float]): Arguments to pass to the function
    
    Returns:
        str | float: The result returned by the called function
    """
    log_function_call(name, args)

    function_dict = {
        "get_weather": get_weather,
        "calculate_area_rectangle": calculate_area_rectangle,
        "search_wikipedia": search_wikipedia
    }

    return function_dict.get(name)(**args)


def get_weather(location: str) -> float:
    """
    Returns fake temperature for the given location

    Args:
        location (str): The name of the city and country

    Returns:
        float: A random temperature between -20.0 and 20.0
    """
    return round(random.uniform(-20, 20), 1)


def calculate_area_rectangle(height: float, width: float) -> float:
    """
    Calculate the area of a rectangle

    Args:
        height (float): Height of the rectangle
        width (float): Width of the rectangle

    Returns:
        float: An area of rectangle
    """
    return height * width


def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for a summary of the given query

    Args:
        query (str): Key words for searching

    Returns:
        str: A summary related to the query
    """
    try:
        return wikipedia.summary(query, sentences = 2)
    except wikipedia.exceptions.PageError:
        return "Page not found"


def _load_log_file(filename: str) -> list:
    """
    Load JSON log data from the given file

    Args:
        filename (str): Path to the JSON log file

    Returns:
        list: A list of log entries
    """
    if not os.path.exists(filename):
        return []
    
    with open(filename, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                data = [data]
            return data
        except json.JSONDecodeError:
            return []
        

def _write_log_file(filename: str, data: list) -> None:
    """
    Write a list of log entries to a JSON file

    Args:
        filename (str): Path to the JSON log file
        data (list): List of log entries to write
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def log_function_call(name: str, args: dict[str, str | float]) -> None:
    """
    Log all function calls to a JSON file

    Args:
        name (str): The name of the function being logged
        args (dict[str, str | float]): Arguments passed to the function
    """
    os.makedirs("logs", exist_ok=True)

    log_data = {
        "type": "function_call",
        "function_name": name,
        "args": args,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"logs/{current_date}.json"

    data = _load_log_file(filename)
    data.append(log_data)
    _write_log_file(filename, data)

def log_chat_session(message: dict[str, str]) -> None:
        """
        Log all chat session to a JSON file

        Args:
            messages (dict[str, str]): Chat message dictionary with keys 'role' and 'content'
        """
        log_data = {
            "type": "chat",
            "messages": message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        os.makedirs("logs", exist_ok=True)

        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"logs/{current_date}.json"

        data = _load_log_file(filename)
        data.append(log_data)
        _write_log_file(filename, data)
