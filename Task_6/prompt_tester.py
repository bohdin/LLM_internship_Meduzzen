import os

from dotenv import load_dotenv
from openai import OpenAI

from prompts import prompts, test_cases
from utils import validate_responses

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL")


client = OpenAI(api_key=API_KEY)


def main() -> None:
    number_test = 10

    for i, prompt in enumerate(prompts, 1):
        counter = 0

        print(f"Prompt {i}: {prompt}")

        for _ in range(number_test):
            try:
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "user", "content": f"{prompt}\n\n{test_cases['text']}"}
                    ],
                )

                result = validate_responses(
                    completion.choices[0].message.content, test_cases["expected"]
                )

                if result:
                    counter += 1
            except:
                pass

        print(f"Prompt {i} success rate: {counter}/{number_test}", end="\n\n")


if __name__ == "__main__":
    main()
