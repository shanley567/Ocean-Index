import json
import jsonschema
from jsonschema import validate

def load_schema():
    with open("schema/unified_dive_schema.json", "r") as f:
        return json.load(f)

def validate_dive(dive_json_path):
    schema = load_schema()

    with open(dive_json_path, "r") as f:
        dive = json.load(f)

    try:
        validate(instance=dive, schema=schema)
        print("✔ Dive JSON is valid.")
    except jsonschema.exceptions.ValidationError as e:
        print("❌ Dive JSON is INVALID.")
        print(e)

if __name__ == "__main__":
    validate_dive("output/unified_dive_01.json")
