import os
from jinja2 import Template

# Configuration
input_dir = 'output'
output_dir = '../mbs_docs'
index_file = 'index.html'

# Function to convert file names
def prettify_file_name(file_name):
    base_name = os.path.splitext(file_name)[0]  # Remove the .html extension
    words = base_name.split('_')  # Split by underscore
    return ' '.join(words)  # Join the words with spaces

# Template for the index.html
# TODO make template files for the HTML, JS, and CSS to declutter the code
template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation Index</title>
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
        h1 span.monkey-icon {
            cursor: pointer;
            display: inline-block;
            vertical-align: middle;
        }
        .component {
            margin-bottom: 20px;
        }
        .component h2 {
            color: #0073e6;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            cursor: pointer;
        }
        .component ul {
            list-style-type: none;
            padding: 0;
            display: none;
        }
        .component ul li {
            margin-bottom: 5px;
        }
        .component ul li a {
            text-decoration: none;
            color: #0073e6;
        }
        .component ul li a:hover {
            text-decoration: underline;
        }
    </style>
        <script>
        function toggleSection(event) {
            const ul = event.target.nextElementSibling;
            if (ul.style.display === 'none' || ul.style.display === '') {
                ul.style.display = 'block';
            } else {
                ul.style.display = 'none';
            }
        }
    </script>
    <script src="animations.js"></script>
    <script src="index_search.js"></script>
    <link rel="stylesheet" href="animations.css">
</head>
<body>
    <div class="container">
        <h1>Monkey<span class="monkey-icon"><img src="../mbs_docs/monkey.png" style="width: 24px; height: auto;"></span>Bread</h1>
        <div class="search">
            <input type="text" id="search-input" placeholder="Search...">
        </div>
        <div id="components">
            {% for component, files in components.items() %}
            <div class="component">
                <h2 onclick="toggleSection(event)">{{ component }}</h2>
                <ul>
                    {% for file in files %}
                    <li><a href="{{ input_dir }}/{{ component }}/{{ file.name }}">{{ file.pretty_name }}</a></li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# Function to generate the index page
def generate_index():
    components = {}

    # Traverse the input directory and collect HTML files
    for root, dirs, files in os.walk(input_dir):
        for directory in sorted(dirs, key=lambda s: s.lower()):
            component_dir = os.path.join(root, directory)
            component_name = os.path.basename(component_dir)
            components[component_name] = []
            for sub_root, sub_dirs, sub_files in os.walk(component_dir):
                for file in sorted(sub_files, key=lambda s: s.lower()):
                    if file.endswith('.html'):
                        pretty_name = prettify_file_name(file)
                        components[component_name].append({'name': file, 'pretty_name': pretty_name})

    # Sort the components dictionary
    sorted_components = dict(sorted(components.items(), key=lambda item: item[0].lower()))

    # Render the template
    template = Template(template_str)
    html_content = template.render(components=sorted_components, input_dir=input_dir)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write the index.html file
    with open(os.path.join(output_dir, index_file), 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Generated {index_file} in {output_dir}")

# Generate the index
generate_index()
