# src/models/wm_group.py

import json

def load_wm_group_match_data(file_path="resources/wm_group_match.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_wm_group_match_data(data, file_path="resources/wm_group_match.json"):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

class WMGroupManager:
    def __init__(self, file_path="resources/wm_group_match.json"):
        self.file_path = file_path
        self.wm_group_data = load_wm_group_match_data(file_path)

    def get_wm_group_data(self):
        return self.wm_group_data

    def update_wm_group_data(self, item_name, matched_data):
        self.wm_group_data[item_name] = matched_data

    def save(self):
        save_wm_group_match_data(self.wm_group_data, self.file_path)