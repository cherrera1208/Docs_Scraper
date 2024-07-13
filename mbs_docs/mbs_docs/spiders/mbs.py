import scrapy
import os
import json
from urllib.parse import urlparse

class MySpider(scrapy.Spider):
    name = 'mbs'
    allowed_domains = ['mbsplugins.eu']
    start_urls = ['https://www.mbsplugins.eu/index.shtml']
    expected_items = {}

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
        
        self.log(f'Saved file {component_main_file}')
        
        # Extract item links and names from the component's index page
        items = []
        for row in response.css('table tr'):
            item_name = row.css('td a::text').get()
            item_link = row.css('td a::attr(href)').get()
            if item_name and item_link:
                items.append(item_name)
                # Follow the link to fetch the subpage
                yield response.follow(item_link, self.parse_sub_page, meta={'output_dir': output_dir, 'item_name': item_name})
        
        # Add items to expected_items dictionary
        self.expected_items[component_name] = items

    def parse_sub_page(self, response):
        # Extract the sub page name from the URL or meta
        sub_page_name = response.meta.get('item_name')
        if not sub_page_name:
            parsed_url = urlparse(response.url)
            sub_page_name = parsed_url.path.split('/')[-1].split('.')[0]
        
        # Retrieve the output directory from meta
        output_dir = response.meta['output_dir']
        
        # Save the sub page HTML
        sub_page_file = os.path.join(output_dir, f'{sub_page_name}.html')
        with open(sub_page_file, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved file {sub_page_file}')

    def closed(self, reason):
        # Save the expected items to a JSON file when the spider closes
        with open('expected_items.json', 'w') as f:
            json.dump(self.expected_items, f, indent=4)
        self.log('Saved expected items to expected_items.json')

# Running the spider should be done in the Scrapy project context, using the Scrapy command:
# scrapy crawl mbs
