import json
import re


def extract_json(text):

    try:
        return json.loads(text)

    except Exception:
        pass

    pattern = r"```json\s*(.*?)\s*```"

    match = re.search(
        pattern,
        text,
        re.DOTALL
    )

    if match:

        json_text = match.group(1)

        return json.loads(json_text)

    raise Exception("No valid JSON found")