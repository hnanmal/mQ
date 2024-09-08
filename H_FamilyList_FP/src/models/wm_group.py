# src/models/wm_group.py

import json
import os

def load_wm_group_match_data(file_path="resources/wm_group_match.json"):
    """Load data from the JSON file with UTF-8 encoding. If the file doesn't exist, return an empty dictionary."""
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist. Creating a new one.")
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_wm_group_match_data(data, file_path="resources/wm_group_match.json"):
    """Save data to the JSON file with UTF-8 encoding."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

class WMGroupManager:
    def __init__(self, file_path="resources/wm_group_match.json"):
        self.file_path = file_path
        self.wm_group_data = load_wm_group_match_data(file_path)

    def get_wm_group_data(self):
        return self.wm_group_data

    def update_wm_group_data(self, item_name, matched_items, locked):
        """Update both matched items and locked status for an item."""
        self.wm_group_data[item_name] = {
            "matched_items": matched_items,
            "locked": locked,
        }

    def save(self):
        """Save the WM group data to the JSON file."""
        save_wm_group_match_data(self.wm_group_data, self.file_path)