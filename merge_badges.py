#!/usr/bin/env python3
import json
import requests
from typing import Dict, Set
import sys

# 👇 الناس اللي تبي تجبر لهم شارة
PROTECTED_IDS = {
   
   "375402345971974147"
   "762103548569059338"
}

YOUR_REPO_FILE = "badges.json"
ORIGINAL_URL = "https://badges.vencord.dev/badges.json"

# ⭐ الشارة اللي تنعطى للي ما عنده ولا شي
FORCED_BADGE = [
    {
        "tooltip": "test",
        "badge": "https://badges.vencord.dev/badges/328520309663727628/1-cf12ca5ca979bb23003fa5ea7e4d70be868804a5.webp"
    }
]

def load_local_file(filepath: str) -> Dict:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def download_original(url: str) -> Dict:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error downloading original badges: {e}")
        sys.exit(1)

def smart_merge(your_data: Dict, original_data: Dict, protected_ids: Set[str]) -> Dict:
    merged = {}

    # نجمع كل الـ IDs
    all_ids = set(original_data) | set(your_data) | set(protected_ids)

    for user_id in all_ids:
        if user_id in protected_ids:
            # 1️⃣ عنده شارة محلية
            if user_id in your_data:
                merged[user_id] = your_data[user_id]

            # 2️⃣ عنده شارة رسمية
            elif user_id in original_data:
                merged[user_id] = original_data[user_id]

            # 3️⃣ ما عنده ولا شي → نعطيه شارة غصب
            else:
                merged[user_id] = FORCED_BADGE
        else:
            # غير محمي → الرسمي فقط
            if user_id in original_data:
                merged[user_id] = original_data[user_id]

    return merged

def save_file(data: Dict, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

def main():
    your_data = load_local_file(YOUR_REPO_FILE)
    original_data = download_original(ORIGINAL_URL)

    merged = smart_merge(your_data, original_data, PROTECTED_IDS)
    save_file(merged, YOUR_REPO_FILE)

    print("✅ تم إعطاء شارة لأي شخص ما عنده شارة")

if __name__ == "__main__":
    main()
