import os
import re

# Configuration
# TODO make template for this HTML
test_dir = 'claris_docs/output'
home_button_html = '''
<style>
    body {
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f9;
        color: #333;
    }
    .container {
        width: 80%;
        margin: auto;
        padding: 20px;
        background-color: #fff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        margin-top: 20px;
    }
    h1 {
        text-align: center;
        color: #0073e6;
        margin-bottom: 20px;
    }
    a {
        text-decoration: none;
        color: #0073e6;
    }
    a:hover {
        text-decoration: underline;
    }
    #home-button {
        position: fixed;
        top: 10px;
        right: 10px;
        background-color: #0073e6;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-family: Arial, sans-serif;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
        z-index: 1000;
    }
    #home-button:hover {
        background-color: #005bb5;
    }
</style>
<a id="home-button" href="../index.html">HOME</a>
'''

# Function to clean up HTML content and add home button
def clean_html_content(html_content):
    # Regex pattern to extract content within the specified div with id="mc-main-content"
    pattern = re.compile(r'(<div[^>]*id="mc-main-content"[^>]*>.*?</div>)', re.DOTALL)
    match = pattern.search(html_content)
    if match:
        content = match.group(1)
        # Wrap content in container and add home button
        content_with_home_button = f'<div class="container">{content}</div>' + home_button_html
        return content_with_home_button
    return None

# Function to clean up all HTML files in the specified directory
def clean_html_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                cleaned_content = clean_html_content(content)
                if cleaned_content:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    print(f"Cleaned and added HOME button to {full_path}")
                else:
                    print(f"No matching content found in {full_path}")

# Clean up all HTML files in the test directory
clean_html_files(test_dir)
