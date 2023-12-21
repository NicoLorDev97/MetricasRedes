import gspread
import pandas as pd

from google_auth_oauthlib.flow import InstalledAppFlow

import os
import desglose as dg

spreadsheet_key = "17Ge3iD3xswqericZ135yf33Jt8fqOg-55GZMw4IuQtk" #Aca definimos la ID de la base de datos, que sera siempre la misma ya que es la base.

def ObtenerUsers(directorio):
    directorio_data = directorio
    archivos = os.listdir(directorio_data)
    users = archivos
    return users
            
def Conexion(spreadsheet_key,worksheet_name):
## Aca conectamos , mediante terminal, los csv a una base de datos, en este caso, un spreedsheet
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret_1_647685613625-joqvshfqn4ppoua87hrpr08k3u1k9hn1.apps.googleusercontent.com.json", 
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
    )
    creds = flow.run_local_server(port=0)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_key)
    worksheet = spreadsheet.worksheet(worksheet_name)
    data = worksheet.get_all_values()
    return data

def Carga(worksheet):
    existing_headers = worksheet.row_values(1)

    if set(existing_headers) == set(dg.df_final.columns):
        worksheet.append_rows(dg.df_final.values.tolist(), value_input_option="RAW")
        print("DataFrame agregado correctamente.")
    else:
        print("Los encabezados del DataFrame no coinciden con los de la hoja de cálculo.")

def ObtenerInicio(user):
    worksheet_name = "User"
    data = Conexion(spreadsheet_key,worksheet_name)
    for item in data:
        if user == item[1]:
            inicio = item[3]
            return inicio

####################################################################
#Este vendria a ser el input, que hoja de la base de datos queres traer 
worksheet_name = "User"
#
inicio = ObtenerInicio("Nicolas")
print(inicio)
