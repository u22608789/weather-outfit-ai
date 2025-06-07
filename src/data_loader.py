# loads and parses mock data
# src/data_loader.py

import json
import os

def load_json(file_name):
    data_path = os.path.join(os.path.dirname(__file__), '../data', file_name)
    with open(data_path, 'r') as f:
        return json.load(f)

def load_users():
    return load_json('mock_users.json')

def load_clothing_items():
    return load_json('mock_clothing.json')
