from rest_framework import serializers
from djangoapp.ingestion.models import NCAADirectory, DirectorySport, EndpointType, DirectorySportAlias

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCAADirectory
        fields = ['id', 'name', 'member_type']

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorySport
        fields = ['id', 'name']

class EndpointTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndpointType
        fields = ['id', 'name']

class SportAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorySportAlias
        fields = ['id', 'ncaa_directory_sport', 'name']