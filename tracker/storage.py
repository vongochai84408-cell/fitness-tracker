import json
import os
from datetime import datetime

from .config import DATA_DIR


def save_training_record(record: dict):
    date = record.get("date") or datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(DATA_DIR, f"{date}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        existing["exercises"].extend(record.get("exercises", []))
        record = existing

    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def load_record_for_date(date: str):
    path = os.path.join(DATA_DIR, f"{date}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
