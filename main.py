from powerbiapi import powerbiAPI
from transform import json_to_df
from datetime import date, timedelta
from utils import now
from config import ms_sharepoint_path
from unidecode import unidecode
from sharepoint import SharePoint
import io

# Instancia Classe para leitura API Power BI
powerbi_api = powerbiAPI()

# Instancia Classe para leitura e escrita no sharepoint
sp = SharePoint()

# Cria range datas
print(f"Preparando variveis iniciais...{now()}")
data_atual = date.today() - timedelta(days=1)
start_date = data_atual.isoformat() + 'T00:00:00Z'
end_date = data_atual.isoformat() + 'T23:59:59Z'

# Faz Consulta dos eventos do ultimo dia
print(f"Consultando API Power BI...{now()}")
eventos = powerbi_api.getActivityEvents(
    start_date, end_date)

# Trata os dados gerados
print(f"Tratandos os dados...{now()}")
df = json_to_df(eventos)


# Salva arquivo em memoria
csv_output = io.StringIO()
df.to_csv(csv_output, index=False)
# Rebobinar o buffer para o início
csv_output.seek(0)

# Grava os dados no Sharepoint
print(f"Salvando dados no Sharepoint...{now()}")

sp.upload_file("00.Evollo/" + ms_sharepoint_path + "/05.Acessos PBI",
               unidecode('activity-events_'+start_date+'_'+end_date+'.csv').replace(':', '_'), csv_output)

print(f"Fim do processo...{now()}")
