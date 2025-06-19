import json

def validate_responses(response: str) -> bool:
    try:
        data = json.loads(response)

        check_json_format = isinstance(data, dict)

        check_keys = bool(data.get("title")) and bool(data.get("features")) and bool(data.get("tags"))

        check_title = isinstance(data.get("title"), str)

        check_features = isinstance(data.get("features"), list)

        check_tags = isinstance(data.get("tags"), list)

        return check_json_format and check_keys and check_title and check_features and check_tags
    except:
        return False