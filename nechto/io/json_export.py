import json


def dumps(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
