import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

class TableHandler:

    @staticmethod
    def find_tables(data):
        html = StringIO(data)
        return pd.read_html(html, flavor='lxml')
    
class HREFHandler:

    def __init__(self, data : list, identifier : str):
        self.data = data
        self.identifier = identifier

    def find_hrefs(self) -> list:
        results = []
        
        for item in tqdm(self.data, desc='Looking for hrefs in object storage data...'):
            paths = []

            html_data = item.get('html_data')

            if not html_data:
                continue

            soup = BeautifulSoup(html_data, 'lxml')
            hrefs = [a.get('href') for a in soup.find_all('a') if a.get('href')]
            if not hrefs:
                continue

            endpoint = item.get('endpoint')

            for href in hrefs:

                resolved = urljoin(endpoint, href)

                if not resolved.startswith(endpoint) or resolved == endpoint:
                    continue

                paths.append({
                    'identifier': item.get(f'{self.identifier}'),
                    'parent_endpoint': item.get('endpoint'),
                    'relative_path': resolved
                })

            results.append(paths)
        
        return results
        