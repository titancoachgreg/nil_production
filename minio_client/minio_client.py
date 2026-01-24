from minio import Minio
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime
import json, os

load_dotenv()

class MinioClient:

    @classmethod
    def get_minio_client(cls):
        return Minio(
            endpoint="minio:9000",
            access_key=os.getenv('MINIO_ROOT_USER'),
            secret_key=os.getenv('MINIO_ROOT_PASSWORD'),
            secure=False,
        )
    
    @classmethod
    def get_minio_data(cls, bucket_name=None, prefix=None):
        client = cls.get_minio_client()

        objects = list(client.list_objects(bucket_name=bucket_name, prefix=prefix, recursive=True))
        if not objects:
            return None
        
        latest_object = max(objects, key=lambda x: x.last_modified)

        response = client.get_object(latest_object.bucket_name, latest_object.object_name)
        try:
            content = response.read().decode('utf-8')
            data = json.loads(content)
        finally:
            response.close()
            response.release_conn()

        return data
    
    @classmethod
    def push_minio_data(cls, data=None, bucket_name=None, sub_bucket=None, identifier=None):
        client = cls.get_minio_client()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        object_key = f"{sub_bucket}/{identifier}/{timestamp}.json"
        data_bytes = json.dumps(data).encode('utf-8')
        data_dump = BytesIO(data_bytes)

        client.put_object(
            bucket_name=bucket_name,
            object_name=object_key,
            data=data_dump,
            length=len(data_bytes),
            content_type='application/json'
        )

    