import json
from pathlib import Path

# Get the directory of the current script
script_dir = Path(__file__).resolve().parent

# Define the paths
input_path = script_dir.parent / 'Structures' / 'maDMP-schema-1.2.json'
output_path = script_dir.parent / 'Structures' / 'maDMP-schema-normalised-lifted.json'


def normalize_oneof(data):
    if not isinstance(data, dict): return data
    if 'oneOf' in data:
        return next((opt for opt in data['oneOf'] if opt.get('type') == 'array'), data['oneOf'][0])
    return {k: normalize_oneof(v) for k, v in data.items()}


def reify_array_containers(data):
    """
    Finds array definitions in $defs and transforms them into object
    wrappers so LinkML recognizes them as Classes.
    """
    if "$defs" not in data:
        return data

    new_defs = {}
    for name, schema in data["$defs"].items():
        # Check if the definition is an array
        if isinstance(schema, dict) and schema.get("type") == "array" and "items" in schema:
            # Transform: Array -> Object with an 'items' property
            new_defs[name] = {
                "type": "object",
                "title": name,
                "properties": {
                    "items": schema  # Keeps the original array definition inside
                }
            }
        else:
            new_defs[name] = schema

    data["$defs"] = new_defs
    return data


if __name__ == "__main__":
    with open(input_path, "r") as f:
        data = json.load(f)

    # 1. Normalize oneOf
    data = normalize_oneof(data)

    # 2. Reify arrays into objects so LinkML sees them as classes
    data = reify_array_containers(data)

    # 4. Deep-clean the properties to ensure $ref usage
    def deep_ref_fix(obj):
        if not isinstance(obj, dict): return obj
        for k, v in obj.items():
            if isinstance(v, dict):
                # If we find a property that matches a def, ensure it's a ref
                if k in data["$defs"] and "$ref" not in v:
                    obj[k] = {"$ref": f"#/$defs/{k}"}
                else:
                    deep_ref_fix(v)
            elif isinstance(v, list):
                obj[k] = [deep_ref_fix(i) if isinstance(i, dict) else i for i in v]
        return obj


    if "properties" in data:
        data["properties"] = deep_ref_fix(data["properties"])

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)