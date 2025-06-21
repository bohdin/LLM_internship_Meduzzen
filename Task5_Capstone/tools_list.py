tools = [
    {
        "type": "function",
        "function": {
            "name": "semantic_search",
            "description": "Search the most relevant information in the specified knowledge base, when the user asks questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's search question.",
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_session",
            "description": "Summarize the conversation between the assistant and the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                        "description": "List of chat messages with roles and content.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {"type": "string"},
                                "content": {"type": "string"},
                            },
                            "required": ["role", "content"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["messages"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]
