import os
from jinja2 import Template

# Configuration
output_dir = 'claris_docs'
index_file = 'claris_docs/index.html'
items_per_page = 20

# Function to convert file names
def prettify_file_name(file_name):
    base_name = os.path.splitext(file_name)[0]  # Remove the .html extension
    words = base_name.split('-')  # Split by hyphen
    return ' '.join(word.capitalize() for word in words)  # Capitalize each word and join with spaces

# Template for the index.html
# TODO make template files for the HTML, JS, and CSS to decluctter the code
template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claris Documentation Index</title>
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
        .search {
            margin-bottom: 20px;
            text-align: center;
        }
        .search input {
            width: 80%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #0073e6;
            color: white;
            text-transform: uppercase;
        }
        td a {
            text-decoration: none;
            color: #0073e6;
        }
        td a:hover {
            text-decoration: underline;
        }
        .pagination {
            margin: 20px 0;
            text-align: center;
        }
        .pagination a {
            margin: 0 5px;
            padding: 8px 16px;
            text-decoration: none;
            background-color: #0073e6;
            color: white;
            border-radius: 4px;
            display: inline-block;
        }
        .pagination a.disabled {
            background-color: #ddd;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Claris Documentation Index</h1>
        <div class="search">
            <input type="text" id="search" placeholder="Search..." oninput="filterFiles()">
        </div>
        <table id="file-table">
            <thead>
                <tr>
                    <th>File Name</th>
                </tr>
            </thead>
            <tbody id="file-list">
                {% for file in files %}
                <tr>
                    <td><a href="{{ file.path }}">{{ file.pretty_name }}</a></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="pagination">
            <span id="pagination"></span>
        </div>
    </div>
    <script>
        let currentPage = 1;
        const itemsPerPage = {{ items_per_page }};
        const tableBody = document.getElementById('file-list');
        const pagination = document.getElementById('pagination');
        const rows = Array.from(tableBody.getElementsByTagName('tr'));

        function renderTable() {
            const totalPages = Math.ceil(rows.length / itemsPerPage);
            rows.forEach((row, index) => {
                row.style.display = (index >= (currentPage - 1) * itemsPerPage && index < currentPage * itemsPerPage) ? '' : 'none';
            });
            renderPagination(totalPages);
        }

        function renderPagination(totalPages) {
            pagination.innerHTML = '';

            const pageLinksToShow = 5;
            const half = Math.floor(pageLinksToShow / 2);
            let startPage = Math.max(currentPage - half, 1);
            let endPage = Math.min(currentPage + half, totalPages);

            if (currentPage <= half) {
                endPage = Math.min(pageLinksToShow, totalPages);
            } else if (currentPage + half >= totalPages) {
                startPage = Math.max(totalPages - pageLinksToShow + 1, 1);
            }

            if (currentPage > 1) {
                const firstPageLink = document.createElement('a');
                firstPageLink.textContent = 'First Page';
                firstPageLink.href = '#';
                firstPageLink.onclick = (event) => {
                    event.preventDefault();
                    currentPage = 1;
                    renderTable();
                };
                pagination.appendChild(firstPageLink);
            }

            for (let i = startPage; i <= endPage; i++) {
                const pageLink = document.createElement('a');
                pageLink.textContent = i;
                pageLink.href = '#';
                pageLink.className = (i === currentPage) ? 'disabled' : '';
                pageLink.onclick = (event) => {
                    event.preventDefault();
                    currentPage = i;
                    renderTable();
                };
                pagination.appendChild(pageLink);
            }

            if (currentPage < totalPages) {
                const lastPageLink = document.createElement('a');
                lastPageLink.textContent = 'Last Page';
                lastPageLink.href = '#';
                lastPageLink.onclick = (event) => {
                    event.preventDefault();
                    currentPage = totalPages;
                    renderTable();
                };
                pagination.appendChild(lastPageLink);
            }
        }

        function filterFiles() {
            const searchTerm = document.getElementById('search').value.toLowerCase();
            let filteredCount = 0;
            rows.forEach(row => {
                const fileName = row.getElementsByTagName('td')[0].textContent.toLowerCase();
                const isMatch = fileName.includes(searchTerm);
                row.style.display = isMatch ? '' : 'none';
                if (isMatch) filteredCount++;
            });
            currentPage = 1; // Reset to the first page
            renderPagination(Math.ceil(filteredCount / itemsPerPage)); // Re-render pagination based on filtered results
        }

        renderTable();
    </script>
</body>
</html>
"""

# Recursively list all HTML files in the output directory
file_list = []
for root, dirs, files in os.walk(output_dir):
    for file in files:
        if file.endswith('.html'):
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, output_dir)
            file_list.append({'name': file, 'path': relative_path, 'pretty_name': prettify_file_name(file)})

# Sort files by name
file_list.sort(key=lambda x: x['name'])

# Render the template
template = Template(template_str)
html_content = template.render(files=file_list, items_per_page=items_per_page)

# Write the index.html file
with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated {index_file}")
