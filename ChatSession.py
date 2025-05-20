from typing import List, Dict
import json
from datetime import datetime
import os

class ChatSession:
    messages: List[Dict[str, str]]
    total_tokens: int
    system_prompt: str

    def __init__(self, prompt):
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

    def add_tokens(self, tokens: int):
        self.total_tokens += tokens

    def save_to_json(self):
        log_data = {
            "system_prompt": self.system_prompt,
            "total_tokens": self.total_tokens,
            "messages": self.messages
        }

        os.makedirs("logs", exist_ok=True)

        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs/{current_date}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)

