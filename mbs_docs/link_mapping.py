import os
from bs4 import BeautifulSoup
import json

# Configuration
output_json = 'updated_anchor_texts.json'
base_dir = 'output'  # Ensure this is the correct directory

def update_html_files(anchor_texts, base_dir):
    for file_path, anchors in anchor_texts.items():
        full_path = os.path.join(base_dir, file_path)
        
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            continue
        
        print(f"Processing file: {full_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Original content length: {len(content)}")

        soup = BeautifulSoup(content, 'html5lib')

        for anchor in anchors:
            original_text = anchor['text']
            new_href = anchor['href']
            
            print(f"Original text: {original_text}, New href: {new_href}")
            
            # Find all relevant anchor tags and update them based on the text
            a_tags = soup.find_all('a')
            for a_tag in a_tags:
                if 'href' in a_tag.attrs and a_tag.get_text() == original_text:
                    print(f"Updating href for {original_text} from {a_tag['href']} to {new_href}")
                    a_tag['href'] = new_href

            # Special handling for component_ links
            if "component_" in new_href:
                component_name = new_href.split('_')[1].replace('.html', '')
                parent_dir = file_path.split('/')[0]
                correct_href = f"../{component_name}/{component_name}.html"
                a_tags = soup.find_all('a', href=new_href)
                for a_tag in a_tags:
                    if 'href' in a_tag.attrs and 'component_' in a_tag['href']:
                        a_tag['href'] = correct_href
                        a_tag.string = component_name
                        print(f"Updated component link: {a_tag}")

        new_content = str(soup)
        print(f"Modified content length: {len(new_content)}")

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f'Updated file: {full_path}')

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Read the updated JSON file
updated_anchor_texts = read_json(output_json)

# Update the HTML files with the new href values
update_html_files(updated_anchor_texts, base_dir)
