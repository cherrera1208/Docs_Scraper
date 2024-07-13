import json

# Configuration
input_json = 'anchor_texts.json'
output_json = 'updated_anchor_texts.json'

def process_anchor_texts(anchor_texts):
    for file_path, anchors in anchor_texts.items():
        for anchor in anchors:
            href = anchor['href']
            text = anchor['text']
            # Extract the parent directory and the file name from the text
            if '.' in text:
                parent_dir, file_name = text.split('.', 1)
                # Update the href with the new format
                anchor['href'] = f"../{parent_dir}/{file_name}.html"
            # Replace .shtml with .html if present
            anchor['href'] = anchor['href'].replace('.shtml', '.html')
    return anchor_texts

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'Updated anchor texts saved to {file_path}')

# Read the JSON file
anchor_texts = read_json(input_json)

# Process the anchor texts
updated_anchor_texts = process_anchor_texts(anchor_texts)

# Write the updated anchor texts back to a JSON file
write_json(updated_anchor_texts, output_json)
