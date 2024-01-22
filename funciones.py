import gspread
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
import desglose
import os
import funciones as f


def ObtenerUsers(directorio):
    directorio_data = directorio
    archivos = os.listdir(directorio_data)
    users = archivos
    return users

def ConexionInicio(spreadsheet_key,worksheet_name1):#worksheet_name2 #Worksheet_Name es para traer que hoja de la base quiero traer
## Aca conectamos , mediante terminal, los csv a una base de datos, en este caso, un spreedsheet
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret_335644978471-31p4l6j7bup27s27a6rgj1djer4uuhgc.apps.googleusercontent.com.json", 
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
    worksheet = spreadsheet.worksheet(worksheet_name1)
   # worksheet2 = spreadsheet.worksheet(worksheet_name2)
    data = worksheet.get_all_values()
    #data2 = worksheet2.get_all_values()
    return data #, data2

def ConexionCarga(spreadsheet_key,worksheet_name):
## Aca conectamos , mediante terminal, los csv a una base de datos, en este caso, un spreedsheet
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret_335644978471-31p4l6j7bup27s27a6rgj1djer4uuhgc.apps.googleusercontent.com.json", 
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
    )
    creds = flow.run_local_server(port=0)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)
    data = sheet.get_all_values()
    spreadsheet = client.open_by_key(spreadsheet_key)
    worksheet = spreadsheet.worksheet(worksheet_name)
    return worksheet

def Carga(worksheet, df):
    existing_headers = worksheet.row_values(1)
    if set(existing_headers) == set(df.columns):
        worksheet.append_rows(df.values.tolist(), value_input_option="RAW")
        print("DataFrame agregado correctamente.")
    else:
        print("Los encabezados del DataFrame no coinciden con los de la hoja de cálculo.")


def ObtenerInicios(spreadsheet_key):
    worksheet_name = "User"
    data = ConexionInicio(spreadsheet_key,worksheet_name)
    return data

def ObtenerInicio(data,user):
    for item in data:
        if user == item[1] + " " + item[2]:
            inicio = item[3]
            return inicio
        
def ObtenerDF(user,df_final,inicio):
    df_final = desglose.Connections(user,df_final,inicio)
    df_final = desglose.Empresas_seguidas(user,df_final,inicio)
    df_final = desglose.Invitaciones(user,df_final,inicio)
    df_final = desglose.Reacciones(user, df_final,inicio)
    df_final = desglose.Publicaciones(user,df_final,inicio)
    df_final = desglose.Inbox(user,df_final,inicio)
    df_final = desglose.Comentarios(user,df_final,inicio)
    return df_final
