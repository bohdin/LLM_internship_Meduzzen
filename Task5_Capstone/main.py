import argparse
import os

import openai
from dotenv import load_dotenv
from rich.console import Console

from chat_session import ChatSession
from vector_store import VectorStore
from tools import tools
from utils import stream_assistant_response, handle_tool_call

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

client = openai.OpenAI(api_key=API_KEY)

parser = argparse.ArgumentParser()
parser.add_argument("--persona", type=str)
args = parser.parse_args()

console = Console()


def main():
    assistant_behavior = args.persona
    system_prompt = (
        f"You are {assistant_behavior} assistant" if assistant_behavior else None
    )
    session = ChatSession(prompt=system_prompt)
    vectors = VectorStore()

    while True:

        user_input = console.input("[blue]You:[/] ")

        if user_input.lower() == "/exit":
            session.save_to_json()
            vectors.save()
            print("Goodbye!")
            break

        try:
            if user_input.lower() == "/update_kb_text":
                console.print(
                    "[dim]Assistant:[/]  Please enter the knowledge text you'd like to store:"
                )
                user_text = console.input("[blue]User:[/] ")
                vectors.add_text(client, user_text)
                continue

            if user_input.lower() == "/update_kb_voice":
                console.print(
                    "[dim]Assistant:[/]  Please enter name of audio file or path:"
                )
                user_audio = console.input("[blue]User:[/] ")
                vectors.add_audio(client, user_audio)
                continue

            session.add_message("user", user_input)

            assistant_reply, tool_calls = stream_assistant_response(
                client, MODEL_NAME, session.messages, tools, console
            )

            if tool_calls:
                for tool_call in tool_calls.values():
                    handle_tool_call(tool_call, session)

                assistant_reply, _ = stream_assistant_response(
                    client, MODEL_NAME, session.messages, tools, console
                )

            session.add_message("assistant", assistant_reply)

            tokens_used = session.count_tokens()
            session.add_tokens(tokens_used)

        except openai.RateLimitError as rate_limit_error:
            console.print(f"[red]Error:[/] {rate_limit_error}")
            print("You got rate limit error. Please wait")

        except openai.APITimeoutError as api_timeout_error:
            console.print(f"[red]Error:[/] {api_timeout_error}")
            print("Problem with connection")


if __name__ == "__main__":
    main()
