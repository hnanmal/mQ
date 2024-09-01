# src/models/configuration.py

import json

def load_config(tree, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_config(config_data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=4)

class ConfigurationManager:
    def __init__(self, config_file="resources/config.json"):
        self.config_file = config_file
        self.config_data = load_config(config_file)

    def get_config(self, key, default=None):
        return self.config_data.get(key, default)

    def set_config(self, key, value):
        self.config_data[key] = value

    def save(self):
        save_config(self.config_data, self.config_file)