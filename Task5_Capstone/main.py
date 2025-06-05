import argparse
import asyncio
import os

import openai
from dotenv import load_dotenv
from openai import AsyncOpenAI
from rich.console import Console
from rich.live import Live
from rich.text import Text

from chat_session import ChatSession
from vector_store import VectorStore

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

client = AsyncOpenAI(api_key=API_KEY)
parser = argparse.ArgumentParser()
parser.add_argument("--persona", type=str)
args = parser.parse_args()

console = Console()

async def main():
    assistant_behavior = args.persona
    system_prompt = f"You are {assistant_behavior} assistant"
    session = ChatSession(prompt=system_prompt)
    vectors = VectorStore()

    model_name = "gpt-4o"

    while True:
        user_input = console.input("[blue]You:[/] ")

        if user_input.lower() == "/exit":
            session.save_to_json()
            vectors.save()
            print("Goodbye!")
            break   

        try:
            if user_input.lower() == "/update_kb_text":
                console.print("[dim]Assistant:[/]  Please enter the knowledge text you'd like to store:")
                user_text = console.input("[blue]User:[/] ")
                await vectors.add_text(client, user_text)
                continue


            session.add_message("user", user_input)

            stream = await client.chat.completions.create(
                model=model_name,
                messages=session.messages,
                stream=True
            )
            
            assistant_reply = ""
            with Live(Text("Assistant is typing...", style="dim"), refresh_per_second=4, console=console) as live:
                async for chunk in stream:
                    if delta := chunk.choices[0].delta.content:
                        assistant_reply += delta
                        text = Text.assemble(("Assistant: ", "dim"), (assistant_reply, "default"))
                        live.update(text)

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
    asyncio.run(main())