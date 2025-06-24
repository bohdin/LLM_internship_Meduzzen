import json
import re
from datetime import datetime


def extract_json(text: str) -> str | None:
    regex_1 = r"```json\s*(\{.*?\})\s*```"
    code_block = re.search(regex_1, text, re.DOTALL)

    if code_block:
        return code_block.group(1)

    regex_2 = r"(\{.*?\})"
    match = re.search(regex_2, text, re.DOTALL)
    if match:
        return match.group(1)

    return None


def validate_responses(response: str, expected: dict) -> bool:
    try:
        json_str = extract_json(response)
        data = json.loads(json_str)

        if not isinstance(data, dict):
            return False

        for key, expected_len in expected.items():
            if key not in data or not isinstance(data[key], list):
                return False
            if len(data[key]) != expected_len:
                return False

        for date in data["dates"]:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except:
                return False

        return True

    except:
        return False
