import scrapy
import os
import json
from urllib.parse import urlparse

class FetchMissingSpider(scrapy.Spider):
    name = 'fetch'
    allowed_domains = ['mbsplugins.eu']
    start_urls = ['https://www.mbsplugins.eu/index.shtml']

    def __init__(self, *args, **kwargs):
        super(FetchMissingSpider, self).__init__(*args, **kwargs)
        # Load expected items from JSON file
        with open('expected_items.json', 'r') as f:
            self.expected_items = json.load(f)

    def parse(self, response):
        # Follow all component links in the main page
        for component_link in response.css('ul > li > a::attr(href)').getall():
            if 'component_' in component_link:
                yield response.follow(component_link, self.parse_component)

    def parse_component(self, response):
        # Extract the component name from the URL
        parsed_url = urlparse(response.url)
        component_name = parsed_url.path.split('_')[-1].split('.')[0]
        
        # Ensure the component directory exists
        output_dir = os.path.join('output', component_name)
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the component's main HTML page
        component_main_file = os.path.join(output_dir, f'{component_name}.html')
        with open(component_main_file, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved main component file {component_main_file}')
        
        # Get the list of expected items for this component
        component_items = self.expected_items.get(component_name, [])
        self.log(f'Expected items for {component_name}: {component_items}')
        
        # Check for missing items
        existing_items = [
            os.path.splitext(file)[0]
            for root, _, files in os.walk(output_dir)
            for file in files if file.endswith('.html')
        ]
        self.log(f'Existing items for {component_name}: {existing_items}')
        
        missing_items = [item for item in component_items if item.split('.')[-1] not in existing_items]
        self.log(f'Missing items for {component_name}: {missing_items}')
        
        # Fetch missing items
        for item in missing_items:
            item_url = f'https://www.mbsplugins.eu/{item.replace(".", "")}.shtml'
            self.log(f'Fetching missing item: {item_url}')
            yield response.follow(item_url, self.parse_sub_page, meta={'output_dir': output_dir, 'item_name': item})

    def parse_sub_page(self, response):
        # Extract the sub page name from the URL or meta
        sub_page_name = response.meta.get('item_name')
        if not sub_page_name:
            parsed_url = urlparse(response.url)
            sub_page_name = parsed_url.path.split('/')[-1].split('.')[0]
        
        # Retrieve the output directory from meta
        output_dir = response.meta['output_dir']
        
        # Save the sub page HTML
        sub_page_file = os.path.join(output_dir, f'{sub_page_name.split(".")[-1]}.html')
        with open(sub_page_file, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved sub page file {sub_page_file}')
