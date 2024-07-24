import requests
import json
from config import ms_powerbi_client_id, ms_powerbi_secret_id, ms_tenant_id
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class powerbiAPI:

    def __init__(
            self, client_id: str = ms_powerbi_client_id, secret_id: str = ms_powerbi_secret_id, tenant_id: str = ms_tenant_id
    ):
        self.client_id = client_id
        self.secret_id = secret_id
        self.tenant_id = tenant_id

    def authenticate(self):

        url = "https://login.microsoftonline.com/" + self.tenant_id + "/oauth2/token/"

        payload = 'client_id=' + self.client_id + '&client_secret=' + self.secret_id + \
            '&scope=openid&grant_type=client_credentials&resource=https%3A%2F%2Fanalysis.windows.net%2Fpowerbi%2Fapi'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        data = json.loads(response.text)

        return data['access_token']

    def getActivityEvents(self, startDate, endDate):

        accessToken = self.authenticate()
        url = "https://api.powerbi.com/v1.0/myorg/admin/activityevents"

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + accessToken
        }

        activity_list = []
        params = "startDateTime='" + startDate + "'&endDateTime='" + endDate + "'"

        while True:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

            data = response.json()

            activity_list.append(data['activityEventEntities'])

            # print(activity_list)

            # Verifica se há mais eventos para serem obtidos
            if data['lastResultSet']:
                break
            else:
                params = {'continuationToken': "'" +
                          data['continuationToken'] + "'"}

        return activity_list
