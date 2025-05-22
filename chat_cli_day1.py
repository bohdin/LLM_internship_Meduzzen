from dotenv import load_dotenv
import os
import asyncio
import openai
from openai import AsyncOpenAI
from ChatSession import ChatSession
import sys
import shutil
import math

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

client = AsyncOpenAI(api_key=API_KEY)



async def main():
    system_prompt = input("System prompt: ")
    session = ChatSession(prompt = system_prompt)

    model_name = "gpt-4o-mini"

    while True:
        user_input = input("You: ")

        
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
            print("Assistant is typing...", flush=True)


            print("Assistant: ", end="", flush=True)
            async for chunk in stream:
                if delta := chunk.choices[0].delta.content:
                    assistant_reply += delta
                    print(delta, end="", flush=True)

            session.add_message("assistant", assistant_reply)

            tokens_used = ChatSession.count_tokens(session.messages)
            session.add_tokens(tokens_used)
            print(f"\n[Tokens used: {tokens_used} | Total so far: {session.total_tokens}]", end="\n\n")

        except openai.RateLimitError as rate_limit_error:
            print(f"Error: {rate_limit_error}")
            print("You got rate limit error. Please wait")

        except openai.APITimeoutError as api_timeout_error:
            print(f"Error: {api_timeout_error}")
            print("Problem with connection")


if __name__ == "__main__":
    asyncio.run(main())