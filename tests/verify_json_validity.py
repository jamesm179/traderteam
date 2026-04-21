import json
import os
import sys

def verify_json_validity():
    invalid_files = []
    json_files = []

    for root, dirs, files in os.walk("."):
        if "node_modules" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))

    if not json_files:
        print("ℹ️ No JSON files found to verify.")
        return True

    for f in json_files:
        try:
            with open(f, 'r') as jf:
                json.load(jf)
        except Exception as e:
            invalid_files.append((f, str(e)))

    if invalid_files:
        print("❌ JSON Validity Check Failed:")
        for f, err in invalid_files:
            print(f"  - {f}: {err}")
        return False

    print(f"✅ All {len(json_files)} JSON files are valid.")
    return True

if __name__ == "__main__":
    if not verify_json_validity():
        sys.exit(1)
