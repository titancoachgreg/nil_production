from djangoapp.ingestion.models import NCAADirectory, DirectorySport, NCAASportDirectory
from minio_client.minio_client import MinioClient
from datetime import datetime

class NCAAHandler:

    @staticmethod
    def upsert_base_data(data):
        obj, created = NCAADirectory.objects.update_or_create(
            external_id=data.get('external_id'),
            defaults={
                'name': data.get('name'),
                'member_type': data.get('member_type'),
                'json_data': data.get('json_data')
            })

    @staticmethod
    def upsert_sport(data):
        obj, created = DirectorySport.objects.update_or_create(
            name=data.get('name'),
            defaults={
                'code': data.get('code'),
                'deleted_at': None
            })

    @staticmethod
    def upsert_internal_sport(data):
        obj, created = NCAASportDirectory.objects.update_or_create(
            ncaa_directory_sport_id=data.get('sport_directory_id'),
            ncaa_directory_id=data.get('directory_id'))

    @staticmethod
    def minio_base_domain(data):
        minio = MinioClient()
        minio.push_minio_data(data=data, 
                              bucket_name='schools', 
                              sub_bucket='base-domain',
                              identifier=data.get('ncaa_directory_id'))

        

