import pandas as pd
import requests
import io
import urllib3

# Evitamos que se llene la consola de warnings por el SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/ITCRMSerie.xlsx"

response = requests.get(url, verify=False)
excel_data = io.BytesIO(response.content)

df = pd.read_excel(excel_data, sheet_name="ITCRM y bilaterales", header=1)
df.columns = df.columns.str.strip()

df = df[["Período", "ITCRM"]].copy()
df.columns = ["fecha", "itcrm"]

df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
df["itcrm"] = pd.to_numeric(df["itcrm"], errors="coerce")

df = df.dropna(subset=["fecha", "itcrm"])

df.to_csv("itcrm.csv", index=False)

print(f"Listo. {len(df)} filas guardadas en itcrm.csv")
print(df.tail())


