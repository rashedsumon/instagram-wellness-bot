import json
import os
from typing import List, Dict
from config import KAGGLE_INSTAGRAM_JSON

def load_instagram_dataset(path: str = None) -> List[Dict]:
    """
    Loads leads / posts from the Kaggle dataset json.
    The dataset structure may vary; adapt the parsing to map to lead fields:
    expected lead keys: name, email, phone, interest, timestamp
    """
    file_path = path or KAGGLE_INSTAGRAM_JSON
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Instagram JSON not found at {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    leads = []
    # Attempt common structures: a list of posts or dict with 'data'
    if isinstance(raw, dict) and "data" in raw and isinstance(raw["data"], list):
        items = raw["data"]
    elif isinstance(raw, list):
        items = raw
    else:
        items = [raw]

    for obj in items:
        # heuristics: try to extract lead fields
        lead = {
            "name": obj.get("name") or obj.get("full_name") or obj.get("user_name") or obj.get("from_name"),
            "email": obj.get("email") or obj.get("contact_email"),
            "phone": obj.get("phone") or obj.get("contact_phone"),
            "interest": obj.get("caption") or obj.get("message") or obj.get("interest"),
            "timestamp": obj.get("timestamp") or obj.get("created_time")
        }
        # Keep only if any contact present
        if lead["email"] or lead["phone"]:
            leads.append(lead)
    return leads

def simulate_new_leads(limit=10):
    leads = load_instagram_dataset()
    # simulate first N as new leads
    return leads[:limit]
