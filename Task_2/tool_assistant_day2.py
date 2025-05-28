import argparse
import json
import os
import random
from datetime import datetime, timezone
from typing import Dict, Union

import wikipedia
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

client = OpenAI(api_key=API_KEY)
parser = argparse.ArgumentParser()
parser.add_argument("-prompt", type=str)
cli_args = parser.parse_args()

tools = [{
    "type": "function",
    "name": "calculate_area_rectangle",
    "description": "Calculating an area for rectangle by given height and width",
    "parameters": {
        "type": "object",
        "properties": {
            "height": { "type": "number"},
            "width": { "type": "number"}
        },
        "required": ["height", "width"],
        "additionalProperties": False
    },
    "strict": True
}, {
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and country e.g. Bogotá, Colombia"
            }
        },
        "required": ["location"],
        "additionalProperties": False
    },
    "strict": True
},{
    "type": "function",
    "name": "search_wikipedia",
    "description": "Search information by given query",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search term e. g. India"
            }
        },
        "required": ["query"],
        "additionalProperties": False
    },
    "strict": True
}]

def main():
    system_prompt = cli_args.prompt

    model_name = "gpt-4o"

    input_messages = [{"role": "system", "content": system_prompt}] if system_prompt else []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break  
        
        input_messages.append({"role": "user", "content": user_input})

        response = client.responses.create(
            model=model_name,
            input=input_messages,
            tools=tools
        )

        check_tools = False
        for tool_call in response.output:
            if tool_call.type != "function_call":
                continue

            check_tools = True
            name = tool_call.name
            args = json.loads(tool_call.arguments)

            formatted_args = ", ".join([f"{k}={repr(v)}" for k, v in args.items()])
            print(f"[GPT triggers {name}({formatted_args})]")

            results = call_function(name, args)
            input_messages.append(tool_call)
            input_messages.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(results)
            })

        if check_tools:
            response = client.responses.create(
                model=model_name,
                input=input_messages,
                tools=tools
            )

        print(f"Assistant: {response.output_text}")
        

def call_function(name: str, args: Dict[str, Union[str, float]]) -> Union[str, float]:
    """
    Calls the appropriate function based on the given function name and arguments

    Args:
        name (str): The name of the function to call
        args (Dict[str, Union[str, float]]): Arguments to pass to the function
    
    Returns:
        Union[str, float]: The result returned by the called function
    """
    save_logs(name, args)

    if name == "get_weather":
        return get_weather(**args)
    if name == "calculate_area_rectangle":
        return calculate_area_rectangle(**args)
    if name == "search_wikipedia":
        return search_wikipedia(**args)

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

def save_logs(name: str, args: Dict[str, Union[str, float]]) -> None:
    """
    Log all function calls to a JSON file

    Args:
        name (str): The name of the function being logged
        args (Dict[str, Union[str, float]]): Arguments passed to the function
    """
    os.makedirs("logs", exist_ok=True)

    log_data = {
        "function_name": name,
        "args": args,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"logs/{current_date}.json"

    data = []

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                if isinstance(existing_data, list):
                    data += existing_data
                else:
                    data.append(existing_data)
            except json.JSONDecodeError: # if file empty
                pass

    data.append(log_data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
