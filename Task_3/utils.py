import os

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


def read_txt(path: str) -> list[tuple[str, str]]:
    """
    Read a .txt file and return its lines with source number

    Args:
        path (str): Path to the text file

    Returns:
        list[tuple[str, str]]: A list of (source ID, line) pairs
    """
    with open(path, "r", encoding="utf-8") as f:
        return [(f"Source #{i}", line.strip()) for i, line in enumerate(f, start=1) if line.strip()]
    

def make_query(query: str, texts: list[str]) -> str:
    """
    Generate a GPT query prompt using an introduction, source articles, and a user question

    Args:
        query (str): The user's input question
        texts (list[str]): A list of relevant text passages from semantic search

    Returns:
        str: A formatted prompt string to send to GPT, including sources and instructions for citation
    """
    introduction = "Use the below articles to answer the subsequent question.\n" + \
        "Cite your sources explicitly using the format 'According to Source #N'. For example: 'According to Source #2, ...'\n" + \
        "Your answer should be a concise summary, using information from the most relevant sources"
    
    question = f"\n\nQuestion: {query}"
    articles = "\n\n".join([text for text in texts])
    return f"{introduction}\n\n{articles}{question}"


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