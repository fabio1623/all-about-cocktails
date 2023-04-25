import requests

class NexibleService:
    def __init__(self):
        self.base_url = 'https://us-central1-nexible-code.cloudfunctions.net'
        
    def get_cocktails(self):
        url = f'{self.base_url}/cocktails'
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch cocktails from Nexible API..")