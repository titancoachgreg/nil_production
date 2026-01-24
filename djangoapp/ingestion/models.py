from django.db import models
from django.utils import timezone

# abstract model
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def delete(self, using=None, keep_parents=False):
        self.soft_delete()

# ingestion models
class NCAADirectory(TimeStampedModel):
    external_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    member_type = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True)

    class Meta:
        db_table = 'ncaa_directory'

class DirectorySport(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'directory_sports'

class NCAASportDirectory(TimeStampedModel):
    ncaa_directory = models.ForeignKey(NCAADirectory, on_delete=models.RESTRICT)
    ncaa_directory_sport = models.ForeignKey(DirectorySport, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'ncaa_sport_directory'

class DirectorySportAlias(TimeStampedModel):
    ncaa_directory_sport = models.ForeignKey(DirectorySport, on_delete=models.RESTRICT, related_name='aliases')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'directory_sport_aliases'

class EndpointType(TimeStampedModel):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'endpoint_types'

class Endpoint(TimeStampedModel):
    ncaa_sport_directory = models.ForeignKey(NCAASportDirectory, on_delete=models.RESTRICT)
    endpoint_type = models.ForeignKey(EndpointType, on_delete=models.RESTRICT)
    endpoint = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'endpoints'

class MinioRelation(models.Model):
    pass