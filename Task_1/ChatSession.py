import json
import os
from datetime import datetime, timezone

import tiktoken


class ChatSession:

    def __init__(self, prompt: str):
        self.total_tokens = 0
        self.messages = []
        self.add_message("system", prompt)

    def add_message(self, role: str, content: str) -> None:
        """
        Add message to the session with role, tokens used, timestamp

        Args:
            role (str): The role of message sender
            content (str): The text of message
        """
        self.messages.append({
            "role": role, 
            "content": content,
            "tokens_used": ChatSession.count_tokens_per_message(content),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    @staticmethod
    def count_tokens_per_message(content: str) -> int:
        """
        Count tokens for message text

        Args:
            content (str): The text to tokenize

        Returns:
            int: The number of tokens
        """
        encoding = tiktoken.get_encoding("o200k_base")
        tokens = len(encoding.encode(content))
        return tokens

    def count_tokens(self) -> int:
        """
        Calculate the total number of tokens that sent to the model

        Returns:
            int: Total number of tokens
        """
        encoding = tiktoken.get_encoding("o200k_base")
        
        tokens = 0
        for message in self.messages:
            tokens += message["tokens_used"]
        return tokens

    def add_tokens(self, tokens: int) -> None:
        """
        Add token count to the total token counter

        Args:
            tokens (int): The number of tokens to add
        """
        self.total_tokens += tokens

    def save_to_json(self) -> None:
        """
        Save the current session data to a JSON file
        """
        log_data = {
            "total_tokens": self.total_tokens,
            "messages": self.messages
        }

        os.makedirs("logs", exist_ok=True)

        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"logs/{current_date}.json"

        data = []

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                    if isinstance(existing_data, list):
                        data += existing_data
                    else:
                        data.append(existing_data)
                except json.JSONDecodeError: # if file empty
                    pass

        data.append(log_data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2) 
            
        print(f"[Conversation saved to {filename}]")
