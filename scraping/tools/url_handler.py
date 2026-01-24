import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
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

            for href in hrefs:
                paths.append({
                    'identifier': item.get(f'{self.identifier}'),
                    'relative_path': urljoin(item.get('endpoint'), href)
                })

            results.append(paths)
        
        return results
        