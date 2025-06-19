import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from utils import call_function, log_chat_session

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

    if input_messages:
        log_chat_session(input_messages[0])

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break  
        
        user_message = {"role": "user", "content": user_input}
        input_messages.append(user_message)
        log_chat_session(user_message)

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
        
        assistant_message = {"role": "assistant", "content": response.output_text}

        input_messages.append(assistant_message)
        log_chat_session(assistant_message)

        print(f"\nAssistant: {response.output_text}", end='\n\n')
        

if __name__ == "__main__":
    main()
