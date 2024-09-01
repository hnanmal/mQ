# src/models/tree_model.py

import json
import os

def load_json_data(file_path):
    """Load JSON data from a file with UTF-8 encoding."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("JSON data loaded successfully.")
            return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def save_json_data(file_path, data):
    """Save data to a JSON file with UTF-8 encoding."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print("Tree view data saved successfully.")
    except Exception as e:
        print(f"Error saving JSON: {e}")
