import re
import json

def extract_json(text: str):
    """
    Robustly extract JSON from text, even if it's wrapped in markers or 
    contains conversational filler.
    """
    if not text:
        return None
        
    # Try to find content between ```json and ```
    json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try to find content between ``` and ```
    generic_match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if generic_match:
        try:
            return json.loads(generic_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try to find the first { and last } (for object) or [ and ] (for list)
    obj_match = re.search(r"(\{.*\})", text, re.DOTALL)
    if obj_match:
        try:
            return json.loads(obj_match.group(1).strip())
        except json.JSONDecodeError:
            pass
            
    list_match = re.search(r"(\[.*\])", text, re.DOTALL)
    if list_match:
        try:
            return json.loads(list_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Last resort: just try to load the whole thing
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None
