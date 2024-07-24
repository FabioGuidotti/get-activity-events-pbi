import os
from dotenv import load_dotenv


load_dotenv()


ms_powerbi_client_id = os.getenv("ms_powerbi_client_id")
ms_powerbi_secret_id = os.getenv("ms_powerbi_secret_id")
ms_tenant_id = os.getenv("ms_tenant_id")
ms_tenant = os.getenv("ms_tenant")

ms_sharepoint_client_id = os.getenv("ms_sharepoint_client_id")
ms_sharepoint_client_secret = os.getenv("ms_sharepoint_client_secret")
ms_sharepoint_site = os.getenv("ms_sharepoint_site")
ms_sharepoint_path = os.getenv("ms_sharepoint_path")