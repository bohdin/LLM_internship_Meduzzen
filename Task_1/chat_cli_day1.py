from dotenv import load_dotenv
import os
import asyncio
import openai
from openai import AsyncOpenAI
from ChatSession import ChatSession
import argparse
from rich.console import Console
from rich.live import Live
from rich.text import Text

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

client = AsyncOpenAI(api_key=API_KEY)
parser = argparse.ArgumentParser()
parser.add_argument("-prompt", type=str)
args = parser.parse_args()

console = Console()

async def main():
    system_prompt = args.prompt or console.input("[bold]System prompt:[/] ")
    session = ChatSession(prompt = system_prompt)

    model_name = "gpt-4o-mini"

    while True:
        user_input = console.input("[blue]You:[/] ")

        
        if user_input.lower() in ["quit", "exit"]:
            session.save_to_json()
            print("Goodbye!")
            break   

        try:
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
            print(f"[Tokens used: {tokens_used} | Total so far: {session.total_tokens}]", end="\n\n")

        except openai.RateLimitError as rate_limit_error:
            console.print(f"[red]Error:[/] {rate_limit_error}")
            print("You got rate limit error. Please wait")

        except openai.APITimeoutError as api_timeout_error:
            console.print(f"[red]Error:[/] {api_timeout_error}")
            print("Problem with connection")


if __name__ == "__main__":
    asyncio.run(main())