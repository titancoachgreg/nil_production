from rest_framework import viewsets
from djangoapp.ingestion.models import NCAADirectory, DirectorySport, DirectorySportAlias, EndpointType
from djangoapp.api.serializers import SportSerializer, SportAliasSerializer, SchoolSerializer, EndpointTypeSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = NCAADirectory.objects.all()
    serializer_class = SchoolSerializer

class SportViewSet(viewsets.ModelViewSet):
    queryset = DirectorySport.objects.all()
    serializer_class = SportSerializer

class EndpointTypeViewSet(viewsets.ModelViewSet):
    queryset = EndpointType.objects.all()
    serializer_class = EndpointTypeSerializer

class SportAliasViewSet(viewsets.ModelViewSet):
    queryset = DirectorySportAlias.objects.all()
    serializer_class = SportAliasSerializer
