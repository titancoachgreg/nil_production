from djangoapp.ingestion.models import NCAADirectory
from scraping.tools.request import Request
from scraping.tools.threading import Threader
from tqdm import tqdm

import logging
logger = logging.getLogger(__name__)

class NCAAClient:

    BASE_URL = 'https://web3.ncaa.org/directory/api/directory/memberList?'
    SUB_URL = 'https://web3.ncaa.org/directory/orgDetail?'
    SPORTS_URL = 'https://web3.ncaa.org/directory/api/common/sportList'

    def fetch_base_data(self) -> list:
        param_types = [1, 3]
        batch = []

        for param_type in param_types:
            results = []

            try: 
                r = Request.get_data(url=self.BASE_URL, params=f'type={param_type}').json()

            except Exception as e:
                logger.error(f'Failed to fetch base data for typ={param_type}', e)
                continue

            for entity in tqdm(r, desc='Fetching base directory data...'):
                external_id = entity.get('orgId')
                sub_r = Request.get_data(url=self.SUB_URL, params=f'id={external_id}')
                entity['sub_html_data'] = sub_r.text
                results.append(entity)

            batch.append(results)

        return batch
    
    def fetch_sport_list(self) -> dict:
        r = Request.get_data(url=self.SPORTS_URL).json()
        return r
    
    @classmethod
    def _fetch_entities(cls):
        return (NCAADirectory.objects
            .filter(member_type=2)
            .values_list('id', 'name', 'json_data')
            .order_by('id')
        )
    
    def fetch_base_domain(cls):

        def fetch(directory):
            directory_id, json_data = directory
            endpoint = f"https://{json_data.get('athleticWebUrl')}"
            response = Request.get_data(endpoint, sleep_enabled=False)
            return {
                'ncaa_directory_id': directory_id,
                'endpoint': endpoint,
                'html_data': response.text if response else None
            }
        
        return Threader.thread_iterable(entities=cls._fetch_entities(), func=fetch)
