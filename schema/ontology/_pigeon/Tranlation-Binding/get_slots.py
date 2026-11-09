import json
from pathlib import Path

# Resolve the directory of the current script
script_dir = Path(__file__).resolve().parent

# Construct the paths relative to the parent of the script directory
base_dir = script_dir.parent

input_path = base_dir / 'Metadata' / 'project_values_nested.json'


def get_keys(data, path=""):
    keys = set()
    if isinstance(data, dict):
        for k, v in data.items():
            keys.add(k)
            keys.update(get_keys(v, k))
    elif isinstance(data, list):
        for item in data:
            keys.update(get_keys(item))
    return keys

with open(input_path, 'r') as f:
    data = json.load(f)

print("Add these to your slots section:")
for key in get_keys(data):
    print(f"  {key}: {{range: string}}")