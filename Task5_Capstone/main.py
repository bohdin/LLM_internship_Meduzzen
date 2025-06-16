import argparse
import os

import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.text import Text

from chat_session import ChatSession
from vector_store import VectorStore
from tools import tools, call_function

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
    system_prompt = f"You are {assistant_behavior} assistant"
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
                console.print("[dim]Assistant:[/]  Please enter the knowledge text you'd like to store:")
                user_text = console.input("[blue]User:[/] ")
                vectors.add_text(client, user_text)
                continue

            if user_input.lower() == "/update_kb_voice":
                console.print("[dim]Assistant:[/]  Please enter name of audio file or path:")
                user_audio = console.input("[blue]User:[/] ")
                vectors.add_audio(client, user_audio)
                continue
                


            session.add_message("user", user_input)

            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=session.messages,
                tools=tools,
                stream=True
            )


            assistant_reply = ""
            final_tool_calls = {}
            with Live(Text("Assistant is typing...", style="dim"), refresh_per_second=10, console=console) as live:
                for chunk in stream:
                    delta = chunk.choices[0].delta

                    if delta.content:
                        assistant_reply += delta.content
                        live.update(Text.assemble(("Assistant: ", "dim"), (assistant_reply, "default")))
                    
                    if delta.tool_calls:
                        for tool_call in delta.tool_calls:
                            index = tool_call.index

                            if index not in  final_tool_calls:
                                final_tool_calls[index] = tool_call

                            final_tool_calls[index].function.arguments += tool_call.function.arguments
                            live.update(Text(f"Assistant is invoking function...", style="dim"))

            for idx, tool_call in final_tool_calls.items():
                console.print(f"\n[bold]Function call #{idx}:[/bold] {tool_call.function.name}")
                console.print(f"Arguments: {tool_call.function.arguments}")

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
