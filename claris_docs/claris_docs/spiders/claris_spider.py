import scrapy
import os
from urllib.parse import urljoin

class ClarisSpider(scrapy.Spider):
    name = 'claris'
    allowed_domains = ['help.claris.com']
    start_urls = ['https://help.claris.com/en/pro-help/content/']

    def parse(self, response):
        # Save the current page
        self.save_page(response)

        # Extract links and follow them if they are within the desired subdomain
        for link in response.css('a::attr(href)').getall():
            absolute_url = urljoin(response.url, link)
            if absolute_url.startswith('https://help.claris.com/en/pro-help/'):
                yield response.follow(absolute_url, self.parse)

    def save_page(self, response):
        # Normalize the URL to create a valid filename
        path = response.url.replace('https://help.claris.com/en/pro-help/content/', '').strip('/')
        if not path or path.endswith('/'):
            path = os.path.join(path, 'index.html')
        elif not path.endswith('.html'):
            path = path + '.html'
        
        filename = os.path.join('claris_docs/output', path)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Write the file
        with open(filename, 'wb') as f:
            f.write(response.body)
