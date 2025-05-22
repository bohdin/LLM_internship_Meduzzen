from typing import List, Dict
import json
from datetime import datetime
import os
import tiktoken

class ChatSession:
    messages: List[Dict[str, str]]
    total_tokens: int
    system_prompt: str

    def __init__(self, prompt: str):
        self.total_tokens = 0
        self.system_prompt = prompt 
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def update_system_prompt(self, new_prompt: str):
        self.system_prompt = new_prompt
        timestamp = datetime.now().isoformat()

        if self.messages[0]["role"] == "system":
            self.messages[0]["content"] = new_prompt
            self.messages[0]["timestamp"] = timestamp

        else:
            self.messages.insert(0, {
                "role": "system", 
                "content": new_prompt,
                "timestamp": timestamp
                })

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role, 
            "content": content,
            "timestamp": datetime.now().isoformat()
            })
        
    @staticmethod
    def count_tokens(messages: List[Dict[str, str]]) -> int:
        encoding = tiktoken.get_encoding("o200k_base")
        tokens_per_message = 3
        tokens = 0
        for message in messages:
            tokens += tokens_per_message
            tokens += len(encoding.encode(message["content"]))
        tokens += 3
        return tokens

    def add_tokens(self, tokens: int):
        self.total_tokens += tokens

    def save_to_json(self):
        log_data = {
            "system_prompt": self.system_prompt,
            "total_tokens": self.total_tokens,
            "messages": self.messages
        }

        os.makedirs("logs", exist_ok=True)

        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"logs/{current_date}.json"

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(log_data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"[Conversation saved to {filename}]")

