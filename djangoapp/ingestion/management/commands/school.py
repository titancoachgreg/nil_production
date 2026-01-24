from django.core.management.base import BaseCommand, CommandError
from scraping.schools.runner import ObjectRunner

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            choices=['get-base-hrefs',
                     'push-base-endpoints',
                     'push-endpoint-data'],
            required=True
        )

    def handle(self, *args, **kwargs):
        mode = kwargs['mode']
        runner = ObjectRunner()
        
        if mode == 'get-base-hrefs':
            self.stdout.write('Running HREF Finder...')
            runner.get_base_hrefs()

        if mode == 'push-base-endpoints':
            self.stdout.write('Pushing base endpoints...')
            runner.push_endpoints()

        if mode == 'push-endpoint-data':
            self.stdout.write('Pushing endpoint data to minio...')
            runner.process_endpoints()
    