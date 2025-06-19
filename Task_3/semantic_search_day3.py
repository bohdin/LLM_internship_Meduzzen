import os

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from utils import get_embeddings, make_query, read_txt, save_log_markdown

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

client = OpenAI(api_key=API_KEY)


def main():
    dimension = 1536

    index = faiss.IndexFlatIP(dimension)

    texts = read_txt("paragraphs.txt")
    if os.path.exists("embeddings.npy"):
        embeddings = np.load("embeddings.npy")
    else:
        embeddings = [get_embeddings(text[1]) for text in texts]
        np.save("embeddings.npy", embeddings)

    index.add(np.array(embeddings))

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        user_input_embedding = get_embeddings(user_input)

        num_match = 3
        results = index.search(np.expand_dims(user_input_embedding, axis=0), num_match)

        text_for_gpt = []
        print(f"\n-> Top {num_match} Matches: ")
        for idx in results[1][0]:
            text = f'[{texts[idx][0]}]: "{texts[idx][1]}"'
            print(text)
            text_for_gpt.append(text)
        print()

        print("Sending results to GPT-4o...")

        query = make_query(user_input, text_for_gpt)

        model_name = "gpt-4o"

        response = client.chat.completions.create(
            model=model_name, 
            messages=[{"role": "user", "content": query}]
        )

        print(f"Assistant: {response.choices[0].message.content}", end="\n\n")

        save_log_markdown(user_input, response.choices[0].message.content)


if __name__ == "__main__":
    main()
