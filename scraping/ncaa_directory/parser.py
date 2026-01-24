
class NCAAParser:

    @staticmethod
    def parse_base_data(data):
        return {
            'external_id': data.get('orgId'),
            'name': data.get('nameOfficial'),
            'member_type': data.get('memberTypeId'),
            'json_data': data
        }
    
    @staticmethod
    def parse_sport(data):
        return {
            'name': data.get('label'),
            'code': data.get('value')
        }
