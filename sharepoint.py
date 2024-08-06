# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 10:23:35 2022

@author: Nielsen C. Damasceno Dantas
"""

# from shareplum import Site, Office365
# from shareplum.site import Version

# import adal
# import msal
# import atexit

# import urllib.parse
import os
import requests
from config import ms_sharepoint_client_id, ms_sharepoint_client_secret, ms_tenant, ms_tenant_id, ms_sharepoint_site
import json
from io import BytesIO
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class SharePoint:

    def __init__(self):

        self.site_url = 'https://{}.sharepoint.com/sites/{}'.format(ms_tenant, ms_sharepoint_site)

    def get_token(self):

        r = requests.post('https://accounts.accesscontrol.windows.net/{}/tokens/OAuth/2'.format(ms_tenant_id), data={
            "grant_type": "client_credentials",
            "resource": "00000003-0000-0ff1-ce00-000000000000/{}.sharepoint.com@{}".format(ms_tenant, ms_tenant_id),
            "client_id": "{}@{}".format(ms_sharepoint_client_id, ms_tenant_id),
            "client_secret": ms_sharepoint_client_secret
        }, verify=False)

        return json.loads(r.content)["access_token"]

    def headers(self):
        return {
            "Accept": "application/json;odata=verbose",
            "Content-Type": "application/json;odata=verbose",
            "Authorization": "Bearer {}".format(self.get_token())
        }

    def upload_file(self, sharepoint_path, file_name, file):

        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('Documentos%20Partilhados/{sharepoint_path}')/Files/add(url='{file_name}', overwrite=true)"
        arquivo_para_subir = file

        r = requests.post(url, headers=self.headers(), data=arquivo_para_subir, verify=False)

        r.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        return r.status_code

    def read_files(self, sharepoint_path, file_name):
        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('Documentos%20Partilhados/{sharepoint_path}')/Files('{file_name}')/$value"

        r = requests.get(url, headers=self.headers())

        content = r.content

        # Use BytesIO para criar um buffer de bytes a partir do conteúdo
        data_buffer = BytesIO(content)

        # Use a biblioteca pandas para ler o CSV do buffer de bytes
        # Altere o separador e o encoding conforme necessário
        df = pd.read_csv(data_buffer, sep='|')

        return df

    def delete_file(self, sharepoint_path, file_name):

        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('Documentos%20Partilhados/{sharepoint_path}')/Files/add(url='{file_name}', overwrite=true)"

        r = requests.delete(url, headers=self.headers())

        return r.status_code

    def view_files(self, sharepoint_path):

        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('Documentos%20Partilhados/{sharepoint_path}')/Files"

        r = requests.get(url, headers=self.headers())

        return json.loads(r.content)['d']['results']
