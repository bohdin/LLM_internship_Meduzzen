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

        for _ in range(10):

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
        
        print(f"Prompt {i} success rate: {counter}/10")



    for i, (system_prompt, prompt) in enumerate(prompts_with_system, start=len(prompts) + 1):

        counter = 0
        for _ in range(10):

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

        print(f"Prompt {i} success rate: {counter}/10")




if __name__ == "__main__":
    main()