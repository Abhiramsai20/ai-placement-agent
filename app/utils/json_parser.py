import json
import re


def _clean_json_str(s: str) -> str:
    # Remove trailing commas before } or ]
    return re.sub(r",\s*([\]}])", r"\1", s)


def extract_json(text):
    if not text or not isinstance(text, str):
        raise Exception("No text provided to json parser")

    # 1. Strip reasoning / thinking tags if present
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    # 2. Try direct json parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # 3. Try markdown code block
    pattern = r"```(?:json)?\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        json_text = match.group(1).strip()
        try:
            return json.loads(json_text)
        except Exception:
            try:
                return json.loads(_clean_json_str(json_text))
            except Exception:
                pass

    # 4. Try finding outermost object or array
    # Object {...}
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        obj_str = text[first_brace : last_brace + 1]
        try:
            return json.loads(obj_str)
        except Exception:
            try:
                return json.loads(_clean_json_str(obj_str))
            except Exception:
                pass

    # Array [...]
    first_bracket = text.find("[")
    last_bracket = text.rfind("]")
    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        arr_str = text[first_bracket : last_bracket + 1]
        try:
            return json.loads(arr_str)
        except Exception:
            try:
                return json.loads(_clean_json_str(arr_str))
            except Exception:
                pass

    raise Exception("No valid JSON found")