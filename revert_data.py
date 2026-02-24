import json
import re

# Read the current data.js
with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the JSON object from data.js
match = re.search(r'const caseData\s*=\s*(\{.*\});?\s*$', text, re.DOTALL)
if not match:
    # Try another way
    start = text.find('{')
    end = text.rfind('}') + 1
    json_str = text[start:end]
else:
    json_str = match.group(1)

data = json.loads(json_str)

# Load the old structure
with open('old_structure.json', 'r', encoding='utf-8') as f:
    old_structure = json.load(f)

# Load the old guide HTML
with open('old_guide.html', 'r', encoding='utf-8') as f:
    old_guide = f.read()

# Update the data dictionary
data['structure'] = old_structure
if '23_player_investigation_guide' in data['documents']:
    data['documents']['23_player_investigation_guide']['body'] = old_guide

# Write the updated data back to data.js
output_js = f"const caseData = {json.dumps(data, indent=2)};\n"
with open('data.js', 'w', encoding='utf-8') as f:
    f.write(output_js)

print("data.js has been successfully reverted.")
