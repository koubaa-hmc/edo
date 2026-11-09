import json
from rdmo_client import Client

# Configuration
# Configuration
URL = 'http://localhost:8484'  # actual URL
TOKEN = '106cac9b5072b7dcfce4c96a2f52cb302b79fb20'  # actual token
PROJECT_ID = 1  # project ID
FLAT_FILE = '../Metadata/project_values_flat.json'
NESTED_FILE = '../Metadata/project_values_nested.json'


def get_full_path_map(attributes):
    """Generates a mapping of attribute ID to hierarchical path."""
    attr_map = {attr['id']: attr for attr in attributes}
    path_map = {}
    for attr in attributes:
        parts = []
        current = attr
        while current:
            parts.append(current.get('key', 'unknown'))
            parent_id = current.get('parent')
            current = attr_map.get(parent_id)
        path_map[attr['id']] = "/".join(reversed(parts))
    return path_map


def nest_data(data_list):
    """Converts a flat list into a nested dictionary (raster)."""
    nested = {}
    for entry in data_list:
        parts = entry['path'].split('/')
        d = nested
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = entry['value']
    return nested


def fetch_and_save():
    client = Client(url=URL, token=TOKEN)

    # 1. Fetch data
    attributes = client.list_attributes()
    path_map = get_full_path_map(attributes)
    values = client.list_project_values(PROJECT_ID)

    # 2. Extract flat list
    flat_data = []
    for v in values:
        attr_id = v.get('attribute')
        flat_data.append({
            "path": path_map.get(attr_id, f"unknown_id_{attr_id}"),
            "value": v.get('text') or v.get('option') or None
        })

    # 3. Write Flat JSON
    with open(FLAT_FILE, 'w', encoding='utf-8') as f:
        json.dump(flat_data, f, indent=4, ensure_ascii=False)

    # 4. Write Nested Raster JSON
    nested_raster = nest_data(flat_data)
    with open(NESTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(nested_raster, f, indent=4, ensure_ascii=False)

    print(f"Export complete:")
    print(f" - Flat data: {FLAT_FILE}")
    print(f" - Nested raster: {NESTED_FILE}")


if __name__ == "__main__":
    fetch_and_save()