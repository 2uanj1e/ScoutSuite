import requests
from ScoutSuite.utils import get_user_agent
from ScoutSuite.core.console import print_exception


class MSFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_header(self):
        token = self.credentials.get_token('ms_graph')['access_token']
        header = {
            'Authorization': 'Bearer ' + token,
            'User-Agent': get_user_agent(),
            'Accept': 'application/json',}
        return header

    def get_conditional_access_policies(self):
        headers = self.get_header()
        url = 'https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies'
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print_exception(f'Failed to get conditional access policies: {e}')
            return None