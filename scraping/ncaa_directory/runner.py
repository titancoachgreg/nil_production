from .client import NCAAClient
from .parser import NCAAParser
from .handler import NCAAHandler
from .internal import NCAAInternal
from tqdm import tqdm

class ScaperRunner():
    
    def __init__(self, client=None, parser=None, handler=None, internal=None):
        self.client = client or NCAAClient()
        self.parser = parser or NCAAParser()
        self.handler = handler or NCAAHandler()
        self.internal = internal or NCAAInternal()

    def process_base(self):
        raw_data = self.client.fetch_base_data()
        for items in raw_data:
            for item in tqdm(items, desc='Parsing and upserting fetched data...'):
                parsed = self.parser.parse_base_data(item)
                self.handler.upsert_base_data(parsed)

    def process_sport(self):
        raw_data = self.client.fetch_sport_list()
        for item in tqdm(raw_data, desc='Parsing and upserting fetched sport data...'):
            parsed = self.parser.parse_sport(item)
            self.handler.upsert_sport(parsed)

    def process_internal_sport(self):
        raw_data = self.internal.fetch_internal_sport_data()
        for item in tqdm(raw_data, desc='Upserting school sports internally...'):
            self.handler.upsert_internal_sport(item)
    
    def process_base_domain(self):
        raw_data = self.client.fetch_base_domain()
        for item in tqdm(raw_data, desc='Pushing base domain data to Minio...'):
            self.handler.minio_base_domain(item)
