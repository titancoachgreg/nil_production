from djangoapp.ingestion.models import Endpoint
from minio_client.minio_client import MinioClient

class SchoolObjectHandler:

    @staticmethod
    def upsert_endpoint(data):
        obj, created = Endpoint.objects.update_or_create(
            endpoint=data.get('endpoint'),
            defaults={
                'ncaa_sport_directory_id': data.get('ncaa_sport_directory_id'),
                'endpoint_type_id': data.get('endpoint_type_id')
            }
        )
    
    @staticmethod
    def minio_endpoint(data):
        minio = MinioClient()
        minio.push_minio_data(data=data,
                              bucket_name='schools',
                              sub_bucket='endpoints',
                              identifier=data.get('endpoint_id'))