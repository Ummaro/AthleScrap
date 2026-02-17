from bs4 import BeautifulSoup
import requests

class Scrapper:
    def __init__(self, url):
        self.url = url
        self.page_content = None

    def fetch_page(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.page_content = response.text
            return self.page_content
        else:
            raise Exception(f"Failed to fetch page: {response.status_code}")
    
    def parse_page(self, page_content=None):
        if not page_content:
            raise Exception("Page content is empty. Fetch the page first.")
        soup = BeautifulSoup(page_content, 'html.parser')
        return soup