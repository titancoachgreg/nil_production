from djangoapp.ingestion.models import Endpoint
from scraping.tools.request import Request
from scraping.tools.threading import Threader

import logging
logger = logging.getLogger(__name__)

class SchoolClient:

    @classmethod
    def _fetch_endpoints(cls):
        return list(
            Endpoint.objects
            .values_list('id', 'endpoint')
            .order_by('id'))
    
    @classmethod    
    def fetch_endpoint_data(cls):

        def fetch(endpoints):
            endpoint_id, endpoint = endpoints
            response = Request.get_data(endpoint, sleep_enabled=True)
            return {
                'endpoint_id': endpoint_id,
                'endpoint': endpoint,
                'html_data': response.text if response else None
            }
        
        return Threader.thread_iterable(entities=cls._fetch_endpoints(), func=fetch)
        
            