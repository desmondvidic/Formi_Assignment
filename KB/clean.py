import json

# Load the existing JSON
with open("kb_store.json", "r") as f:
    data = json.load(f)

# Process entries
for entry in data:
    city = entry["city"]
    if "delhi" not in city.lower() and "bangalore" not in city.lower():
        # Append original city info to the chunk
        entry["chunk"] = f"{city}\n{entry['chunk']}"
        entry["city"] = "Delhi _ Bangalore _ Bengaluru"

# Write the updated data back
with open("app/kb_store.json", "w") as f:
    json.dump(data, f, indent=2)
