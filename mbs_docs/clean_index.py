import os

# Configuration
output_dir = 'output'  # Replace with the correct path to your output directory

def clean_redundant_files(dir_path):
    for root, _, files in os.walk(dir_path):
        parent_dir = os.path.basename(root)

        prefixed_files = {}
        non_prefixed_files = set()

        # Collect prefixed and non-prefixed file names
        for file in files:
            if file.endswith('.html'):
                file_base = os.path.splitext(file)[0]
                if file_base.startswith(parent_dir):
                    # Store prefixed file and its stripped version
                    stripped_file_base = file_base[len(parent_dir):].lstrip('.')
                    prefixed_files[stripped_file_base] = os.path.join(root, file)
                else:
                    # Store non-prefixed file base
                    non_prefixed_files.add(file_base)

        # Identify and remove redundant prefixed files
        for stripped_file_base, file_path in prefixed_files.items():
            if stripped_file_base in non_prefixed_files:
                os.remove(file_path)
                print(f'Removed redundant file: {file_path}')

# Clean redundant files in the output directory
clean_redundant_files(output_dir)
