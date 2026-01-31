from minio_client.minio_client import MinioClient
from djangoapp.ingestion.models import NCAADirectory, DirectorySport, NCAASportDirectory, Endpoint, EndpointType
from scraping.tools.url_handler import HREFHandler
from tqdm import tqdm
import re

class SchoolEndpoint:

    minio_client = MinioClient()

    @classmethod
    def _fetch_ncaa_entities(cls) -> list:
        return (NCAADirectory
                .objects
                .filter(member_type=2)
                .values_list('id', flat=True)
                .order_by('id'))
    
    @classmethod    
    def _fetch_ncaa_sports_and_aliases(cls) -> tuple:
        return (DirectorySport
                .objects
                .filter(aliases__name__isnull=False)
                .values_list('id','aliases__name'))
    
    @classmethod
    def _fetch_endpoint_types(cls) -> tuple:
        return (EndpointType
                .objects
                .values_list('id', 'name'))
    
    @classmethod
    def _fetch_ncaa_sport_directory(cls) -> tuple:
        return (NCAASportDirectory
                .objects
                .values_list(
                    'id',
                    'ncaa_directory_id',
                    'ncaa_directory_sport_id'
                ))
    
    @classmethod
    def _fetch_endpoints(cls) -> list:
        return (Endpoint
                .objects
                .values_list('id', flat=True)
                .order_by('id'))

    @classmethod
    def _fetch_base_domain_object(cls) -> list:
        results = []
        
        for directory_id in tqdm(cls._fetch_ncaa_entities(), desc='Fetching objects for school base domains...'):
            fetched_object = (cls.
                              minio_client.
                              get_minio_data(bucket_name='schools', 
                                             prefix=f'base-domain/{directory_id}/'))
            
            results.append(fetched_object)
            
        return results
    
    @classmethod
    def _fetch_endpoint_object(cls) -> list:
        results = []

        endpoints = cls._fetch_endpoints()
        
        for endpoint_id in tqdm(endpoints, desc='Fetching objects for school endpoints...'):
            fetched_object = (cls.minio_client.get_minio_data(bucket_name='schools', 
                                             prefix=f'endpoints/{endpoint_id}/'))
            
            results.append(fetched_object)
            
        return results

    @classmethod 
    def _fetch_hrefs(cls) -> list:

        return HREFHandler(cls._fetch_base_domain_object(), 'ncaa_directory_id').find_hrefs()
    
    @classmethod
    def classify_hrefs(cls) -> list:

        alias_to_sport = {}
        for sport_id, alias_name in cls._fetch_ncaa_sports_and_aliases():
            if alias_name:
                alias_to_sport[alias_name.lower()] = sport_id

        type_lookup = {
            type_name.lower(): type_id 
            for type_id, type_name in cls._fetch_endpoint_types()
            if type_name
        } 

        matching_endpoints = []

        for href in tqdm(cls._fetch_hrefs(), desc='Parsing and classifying hrefs...'):
            for item in href:
                child_url = item.get('relative_path')
                matched_sport_id = None
                for alias, sport_id in alias_to_sport.items():
                    pattern = r'\b' + re.escape(alias) + r'\b'
                    if re.search(pattern, child_url):
                        matched_sport_id = sport_id
                        break

                if not matched_sport_id:
                    continue

                matched_type_id = None
                for type_name, type_id in type_lookup.items():
                    if type_name in child_url:
                        matched_type_id = type_id
                        break

                if not matched_type_id:
                    continue

                result = {
                    'ncaa_directory_id': item.get('identifier'),
                    'ncaa_directory_sport_id': matched_sport_id,
                    'endpoint': item.get('relative_path'),
                    'endpoint_type_id': matched_type_id
                }

                matching_endpoints.append(result)
 
        return matching_endpoints
    
    @classmethod
    def map_endpoints(cls) -> list:

        mapping = {
            (directory_id, directory_sport_id): sport_directory_id
            for sport_directory_id, directory_id, directory_sport_id in cls._fetch_ncaa_sport_directory()
        }

        mapped_endpoints = []

        for item in cls.classify_hrefs():
            key = (item.get('ncaa_directory_id'), item.get('ncaa_directory_sport_id'))
            
            matched_sport_directory_id = mapping.get(key)
            
            if matched_sport_directory_id is None:
                continue
            
            result = {
                'ncaa_sport_directory_id': matched_sport_directory_id,
                'endpoint_type_id': item.get('endpoint_type_id'),
                'endpoint': item.get('endpoint')
                }
            
            mapped_endpoints.append(result)
        
        return mapped_endpoints
        