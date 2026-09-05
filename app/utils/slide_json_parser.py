import json
import re


def _clean_json_str(s: str) -> str:
    # Remove trailing commas before } or ]
    return re.sub(r",\s*([\]}])", r"\1", s)


def extract_slide_json(text):
    if not text or not isinstance(text, str):
        raise Exception("No text provided to slide parser")

    # 1. Strip reasoning / thinking tags if present
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    # 2. Try direct parse
    try:
        data = json.loads(text)
        if isinstance(data, list) and len(data) > 0:
            return data
        if isinstance(data, dict):
            for key in ["slides", "data", "presentation", "result"]:
                if key in data and isinstance(data[key], list) and len(data[key]) > 0:
                    return data[key]
    except Exception:
        pass

    # 3. Extract markdown code block if present
    code_block_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if code_block_match:
        block_text = code_block_match.group(1).strip()
        try:
            data = json.loads(block_text)
            if isinstance(data, list) and len(data) > 0:
                return data
            if isinstance(data, dict):
                for key in ["slides", "data", "presentation"]:
                    if key in data and isinstance(data[key], list):
                        return data[key]
        except Exception:
            try:
                data = json.loads(_clean_json_str(block_text))
                if isinstance(data, list) and len(data) > 0:
                    return data
            except Exception:
                pass

    # 4. Find array between [ and ]
    first_bracket = text.find("[")
    last_bracket = text.rfind("]")
    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        candidate = text[first_bracket : last_bracket + 1]
        try:
            data = json.loads(candidate)
            if isinstance(data, list) and len(data) > 0:
                return data
        except Exception:
            try:
                data = json.loads(_clean_json_str(candidate))
                if isinstance(data, list) and len(data) > 0:
                    return data
            except Exception:
                pass

    # 5. Handle truncated array (starts with [ but was cut off before closing ])
    if first_bracket != -1:
        truncated = text[first_bracket:]
        last_brace = truncated.rfind("}")
        if last_brace != -1:
            repaired = _clean_json_str(truncated[: last_brace + 1] + "\n]")
            try:
                data = json.loads(repaired)
                if isinstance(data, list) and len(data) > 0:
                    return data
            except Exception:
                pass

    # 6. Regex object extraction: find individual slide objects
    object_pattern = re.compile(
        r'{\s*"title"\s*:\s*"([^"]+)"\s*,\s*"content"\s*:\s*\[(.*?)\]\s*}',
        re.DOTALL
    )
    slides = []
    for m in object_pattern.finditer(text):
        title = m.group(1).strip()
        raw_content = m.group(2).strip()
        items = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', raw_content)
        if title:
            slides.append({
                "title": title,
                "content": items if items else [f"Preparation guidance for {title}"]
            })

    if len(slides) > 0:
        return slides

    raise Exception("No valid slide JSON found")