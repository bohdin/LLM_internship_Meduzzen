import os
from typing import List

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

client = OpenAI(api_key=API_KEY)

def get_embeddings(text: str) -> np.ndarray:
    """
    Generate normalized embedding vector from input text

    Args:
        text (str): Text to embed

    Returns:
        np.ndarray: A normalized NumPy array of text embedding
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    vector = np.array(response.data[0].embedding)

    return vector / np.linalg.norm(vector)


def read_txt(path: str) -> List[str]:
    """
    Read a .txt file and return its lines

    Args:
        path (str): Path to the text file

    Returns:
        List[str]: A list of non-empty lines
    """
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
    

def make_query(query: str, texts: List[str]) -> str:
    """
    Generate a GPT query prompt using an introduction, source articles, and a user question

    Args:
        query (str): The user's input question
        texts (List[str]): A list of relevant text passages from semantic search

    Returns:
        str: A formatted prompt string to send to GPT, including sources and instructions for citation
    """
    introduction = "Use the below articles to answer the subsequent question.\n" + \
        "Cite your sources explicitly using the format 'According to Source #N'. For example: 'According to Source #2, ...'\n" + \
        "Your answer should be a consice summary, using information from the most relevant sources"
    
    question = f"\n\nQuestion: {query}"
    articles = "\n\n".join([f"Source #{i}: {text}" for i, text in enumerate(texts, start=1)])
    return f"{introduction}\n\n{articles}{question}"


def main():
    dimension = 1536

    index = faiss.IndexFlatIP(dimension)

    texts = read_txt("paragraphs.txt")
    if os.path.exists("embeddings.npy"):
        embeddings = np.load("embeddings.npy")
    else:
        embeddings = [get_embeddings(text) for text in texts]
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
        for i, idx in enumerate(results[1][0], start=1):
            print(f'[{i}] "{texts[idx]}"')
            text_for_gpt.append(texts[idx])
        print()

        print("Sending results to GPT-4o...")

        query = make_query(user_input, text_for_gpt)

        model_name = "gpt-4o"

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": query}
            ]
        )


        print(f"Assistant: {response.choices[0].message.content}", end="\n\n")

        save_log_markdown(user_input, response.choices[0].message.content)


def save_log_markdown(user_input: str, gpt_response: str) -> None:
    """
    Log a question and GPT answer to a Markdown file

    Args:
        user_input (str): The user's input question
        gpt_response (str): The GPT-generated response
    """
    os.makedirs("logs", exist_ok=True)

    file_path = "logs/chat_log.md"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"**User query:** {user_input}\n")
        f.write(f"**GPT answer:** {gpt_response}\n\n")


if __name__ == "__main__":
    main()
