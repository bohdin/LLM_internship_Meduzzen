from openai import OpenAI
from dotenv import load_dotenv
import os
from prompts import prompts, prompts_with_system
from utils import validate_responses

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL")


client = OpenAI(api_key=API_KEY)

def main() -> None:
    for i, prompt in enumerate(prompts, 1):
        counter = 0
        number_test = 10

        print(f"Test: {prompt}")

        for _ in range(number_test):

            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = validate_responses(completion.choices[0].message.content)

            if result:
                counter += 1

        print(f"Prompt {i} success rate: {counter}/{number_test}")



    for i, (system_prompt, prompt) in enumerate(prompts_with_system, start=len(prompts) + 1):

        counter = 0

        print("Test:")
        print(f"System: {system_prompt}")
        print(f"User: {prompt}")

        for _ in range(number_test):

            completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            
            result = validate_responses(completion.choices[0].message.content)

            if result:
                counter += 1
        print(completion.choices[0].message.content)
        print(f"Prompt {i} success rate: {counter}/{number_test}")




if __name__ == "__main__":
    main()