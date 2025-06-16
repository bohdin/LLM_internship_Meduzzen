import argparse
import os

import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.text import Text

from chat_session import ChatSession
from vector_store import VectorStore

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL")

client = openai.OpenAI(api_key=API_KEY)
vector_store = VectorStore()

tools = [{
    "type": "function",
    "function": {
        "name": "semantic_search",
        "description": "Search the most relevant information via knowledge base.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's search question."
                },

                "top_k": {
                    "type": ["integer", "null"],
                    "description": "Number of top results to return (optional). If don't mantion use null."
                }
            },
            "required": ["query", "top_k"],
            "additionalProperties": False
        },
        "strict": True
    }
}]


def call_function(name: str, args: dict[str, str | float]) -> str | float:
    """
    Calls the appropriate function based on the given function name and arguments

    Args:
        name (str): The name of the function to call
        args (dict[str, str | float]): Arguments to pass to the function
    
    Returns:
        str | float: The result returned by the called function
    """

    function_dict = {
        "semantic_search": semantic_search,
    }

    return function_dict.get(name)(**args)

def semantic_search(query: str, top_k: int = 3) -> str:
    results = vector_store.search(client, query, top_k=top_k)
    return make_query(query, results)

def make_query(query: str, texts: list[tuple[int, str]]) -> str:
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
    articles = "\n\n".join([f"Source #{idx} {text}" for idx, text in texts])
    return f"{introduction}\n\n{articles}{question}"