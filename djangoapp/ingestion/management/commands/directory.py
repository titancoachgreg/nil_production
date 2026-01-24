from django.core.management.base import BaseCommand, CommandError
from scraping.ncaa_directory.runner import ScaperRunner

class Command(BaseCommand):

    help = 'Run NCAA Directory scraper'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            choices=['master', 
                     'base', 
                     'sport-list', 
                     'push-sport-list',
                     'sport-internal',
                     'base-domain'],
            required=True
        )
    
    def handle(self, *args, **kwargs):
        mode = kwargs['mode']
        runner = ScaperRunner()

        if mode == 'master':
            self.stdout.write('Running scraping pipeline...')
            runner.process_base()
            runner.process_sport()
            runner.process_internal_sport()
            runner.process_base_domain()

        elif mode == 'base':
            self.stdout.write('Running base data scrape...')
            runner.process_base()

        elif mode == 'sport-list':
            self.stdout.write('Running sport scraper...')
            runner.process_sport()

        elif mode == 'sport-internal':
            self.stdout.write('Running internal sport transfer...')
            runner.process_internal_sport()

        elif mode == 'base-domain':
            self.stdout.write('Running base domain scraper...')
            runner.process_base_domain()

        else:
            raise CommandError(f'Unknown mode: {mode}')

