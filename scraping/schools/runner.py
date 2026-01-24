from .internal import SchoolEndpoint
from .handler import SchoolObjectHandler
from .client import SchoolClient
from tqdm import tqdm

class ObjectRunner():
    
    def __init__(self, object=None, client=None, handler=None):
        self.object = object or SchoolEndpoint()
        self.client = client or SchoolClient()
        self.handler = handler or SchoolObjectHandler()

    def get_base_hrefs(self):
        self.object.classify_hrefs()

    def push_endpoints(self):
        endpoints = self.object.map_endpoints()
        for endpoint in tqdm(endpoints, desc='Pushing base endpoints...'):
            self.handler.upsert_endpoint(endpoint)

    def process_endpoints(self):
        raw_data = self.client.fetch_endpoint_data()
        for item in tqdm(raw_data, desc='Pushing endpoint data to minio...'):
            self.handler.minio_endpoint(item)

