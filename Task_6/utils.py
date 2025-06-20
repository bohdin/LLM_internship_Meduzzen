import json
import re

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

def validate_responses(response: str) -> bool:
    try:
        json_str = extract_json(response)

        data = json.loads(json_str)

        check_json_format = isinstance(data, dict)

        check_keys = bool(data.get("title")) and bool(data.get("features")) and bool(data.get("tags"))

        check_title = isinstance(data.get("title"), str)

        check_features = isinstance(data.get("features"), list)

        check_tags = isinstance(data.get("tags"), list)

        return check_json_format and check_keys and check_title and check_features and check_tags
    except:
        return False