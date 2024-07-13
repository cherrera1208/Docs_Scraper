import os
import re

# Configuration
output_dir = 'output'  # Replace with the correct path to your output directory

# Template for the modernized HTML with a clickable title for the home button
# TODO make template for this HTML
modern_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
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
        h1, h2, h3 {
            color: #0073e6;
        }
        .content {
            margin-top: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f4f4f9;
        }
        .prototype {
            padding: 15px;
            margin: 10px 0;
            border-color: #c4c4c4;
            border-width: 1px;
            border-style: solid;
            background-color: #fffedd;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><a href="../../index.html" style="text-decoration: none; color: #0073e6;">{{ title }}</a></h1>
        <div class="content">
            {{ content }}
        </div>
    </div>
</body>
</html>
"""

def modernize_html_content(content, title):
    # Extract the relevant content within <main> tags
    main_content_match = re.search(r'<main>(.*?)</main>', content, re.DOTALL)
    if main_content_match:
        main_content = main_content_match.group(1)
    else:
        print("No <main> tags found.")
        return content  # Return unchanged content if <main> tags are not found

    # Remove the 'HelpNavigation' table
    main_content = re.sub(r'<table[^>]*class="HelpNavigation"[^>]*>.*?</table>', '', main_content, flags=re.DOTALL)

    # Expand the 'PrototypeBig' section by default and remove the 'Less' link
    main_content = re.sub(
        r'<div id="PrototypeSmall"[^>]*>.*?</div>\s*<div id="PrototypeBig"([^>]*)style="display: none;([^>]*)>(.*?)&nbsp; <a href="#" onClick="lessDocumentation\(\);"[^>]*>Less</a></div>',
        r'<div id="PrototypeBig"\1style="display: block;\2>\3</div>',
        main_content,
        flags=re.DOTALL
    )

    # Handle 'See also', 'Examples', and 'Description' sections
    see_also_match = re.search(r'(<h3 lang="en">See also</h3>\s*<ul translate="no">.*?</ul>)', main_content, re.DOTALL)
    if see_also_match:
        main_content = main_content[:see_also_match.end()]
    else:
        examples_match = re.search(r'(<h3 lang="en">Examples</h3>.*?)(<h3 lang="en">|$)', main_content, re.DOTALL)
        if examples_match:
            main_content = main_content[:examples_match.end(1)]
        else:
            description_match = re.search(r'(<h3 lang="en">Description</h3>.*?)(<h3 lang="en">|$)', main_content, re.DOTALL)
            if description_match:
                main_content = main_content[:description_match.end(1)]

    # Inject the cleaned and modernized content into the template
    modernized_content = modern_template.replace("{{ title }}", title).replace("{{ content }}", main_content)
    return modernized_content

def modernize_files_in_dir(dir_path):
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                title_match = re.search(r'<title>(.*?)</title>', "Monkey🐵Bread🥖Docs📑")
                title = title_match.group(1) if title_match else "Monkey🐵Bread🥖Docs📑"

                modernized_content = modernize_html_content(content, title)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modernized_content)
                
                print(f'Modernized file: {file_path}')

# Modernize files in the output directory
modernize_files_in_dir(output_dir)
