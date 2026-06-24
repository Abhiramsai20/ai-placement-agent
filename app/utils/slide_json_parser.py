import json
import re


def extract_slide_json(text):

    try:
        return json.loads(text)

    except Exception:
        pass

    match = re.search(
        r"\[\s*{.*}\s*\]",
        text,
        re.DOTALL
    )

    if match:

        return json.loads(
            match.group(0)
        )

    raise Exception(
        "No valid slide JSON found"
    )