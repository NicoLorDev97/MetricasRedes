import gspread
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
import desglose
import os

def ObtenerUsers(directorio):
    directorio_data = directorio

    archivos = os.listdir(directorio_data)
    archivos_usuarios = [archivo for archivo in archivos if archivo.endswith('.csv')]
    users = []

    for usuario in archivos_usuarios:
        ruta_usuario = os.path.join(directorio_data, usuario)
        user = usuario.split("_")[0]
        if not user in users:
            users.append(user)
        try:
            with open(ruta_usuario, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            print(f"Procesando usuario: {usuario}")
        
        except UnicodeDecodeError as e:
            print(f"Error al decodificar el archivo {usuario}: {e}")
            
def Conexion(spreadsheet_key,worksheet_name):
## Aca conectamos , mediante terminal, los csv a una base de datos, en este caso, un spreedsheet
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret_258260523243-d55smov40jlgkqdpar7lduol6ua4k81v.apps.googleusercontent.com.json", 
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
    )
    creds = flow.run_local_server(port=0)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("17Ge3iD3xswqericZ135yf33Jt8fqOg-55GZMw4IuQtk").worksheet("Datos")
    data = sheet.get_all_values()
    spreadsheet = client.open_by_key(spreadsheet_key)
    worksheet = spreadsheet.worksheet(worksheet_name)
    return worksheet

def Carga(worksheet):
    existing_headers = worksheet.row_values(1)

    df_resumen = pd.DataFrame(desglose.df_resumen)

    if set(existing_headers) == set(df_resumen.columns):
        worksheet.append_rows(df_resumen.values.tolist(), value_input_option="RAW")
        print("DataFrame agregado correctamente.")
    else:
        print("Los encabezados del DataFrame no coinciden con los de la hoja de cálculo.")


####################################################################
spreadsheet_key = "17Ge3iD3xswqericZ135yf33Jt8fqOg-55GZMw4IuQtk"
worksheet_name = "Datos"
worksheet = Conexion(spreadsheet_key,worksheet_name)
Carga(worksheet)
