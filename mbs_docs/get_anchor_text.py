import os
import json
from bs4 import BeautifulSoup

# Configuration
output_json = 'anchor_texts.json'
base_dir = 'output'

def extract_anchor_texts(base_dir):
    anchor_texts = {}

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                soup = BeautifulSoup(content, 'html.parser')
                anchors = soup.find_all('a', href=True)

                file_anchor_texts = []
                for anchor in anchors:
                    href = anchor['href']
                    text = anchor.get_text()
                    if 'index' not in href and 'newversion' not in href:
                        file_anchor_texts.append({'href': href, 'text': text})

                if file_anchor_texts:
                    # Save the relative file path as the key
                    relative_file_path = os.path.relpath(file_path, base_dir)
                    anchor_texts[relative_file_path] = file_anchor_texts

    return anchor_texts

def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'Anchor texts saved to {file_path}')

# Extract anchor texts
anchor_texts = extract_anchor_texts(base_dir)

# Write the anchor texts to a JSON file
write_json(anchor_texts, output_json)
