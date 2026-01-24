from djangoapp.ingestion.models import NCAADirectory, DirectorySport
from ..tools.url_handler import TableHandler
from tqdm import tqdm

class NCAAInternal:

    @classmethod
    def _fetch_entities(cls):
        return (NCAADirectory.objects
            .filter(member_type=2)
            .values_list('id', 'name', 'json_data')
            .order_by('id'))

    @classmethod
    def _fetch_dir_sports(cls):
        return (DirectorySport.objects
            .values_list('id', 'name')
            .order_by('id'))

    @classmethod
    def fetch_internal_sport_data(cls):
        
        sport_lists = []

        for directory_id, _, json_data in tqdm(cls._fetch_entities(), desc='Fetching school sport data...'):
            html_data = json_data.get('sub_html_data')

            tables = TableHandler.find_tables(html_data)
            sports_table = tables[2] #sports table is the second table in the directory page

            for _, row in sports_table.iterrows():
                sport_name = row['Sport']
                for sport_directory_id, dir_sport in cls._fetch_dir_sports():
                    if not dir_sport:
                        continue
                    
                    if dir_sport == sport_name:
                        directory_uspert = {
                            'directory_id': directory_id,
                            'sport_directory_id': sport_directory_id
                        }
                        sport_lists.append(directory_uspert)

        return sport_lists
