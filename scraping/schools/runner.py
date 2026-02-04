from .internal import SchoolBaseEndpoint, SchoolEndpoint
from .handler import SchoolObjectHandler
from .client import SchoolClient
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

class ObjectRunner():
    
    def __init__(self, object=None, sub_object=None, client=None, handler=None):
        self.object = object or SchoolBaseEndpoint()
        self.sub_object = sub_object or SchoolEndpoint()
        self.client = client or SchoolClient()
        self.handler = handler or SchoolObjectHandler()

    def get_base_hrefs(self):
        self.object.classify_hrefs()

    def test_get_hrefs(self):
        self.sub_object.test_hrefs()

    def push_endpoints(self):
        endpoints = self.object.map_endpoints()
        for endpoint in tqdm(endpoints, desc='Pushing base endpoints...'):
            try:
                self.handler.upsert_endpoint(endpoint)
            
            except Exception as e:
                logger.error(f"Failed to upsert endpoint {endpoint}: {e}", exc_info=True)

    def process_endpoints(self):
        raw_data = self.client.fetch_endpoint_data()
        for item in tqdm(raw_data, desc='Pushing endpoint data to minio...'):
            self.handler.minio_endpoint(item)

