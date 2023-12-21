import pandas as pd
from pandas import merge
import re
import os
import streamlit as st
import matplotlib.pyplot as plt

df_final= pd.DataFrame(columns=['UserId', 'InteraccionId', 'Cantidad', 'Fecha'])

def leer_archivo(ruta,skiprows=0, sheet_name=None):
    extension = os.path.splitext(ruta)[1]
    if extension == '.csv':
        return pd.read_csv(ruta, skiprows=skiprows)
    elif extension == '.xlsx':
        if sheet_name:
            return pd.read_excel(ruta, skiprows=skiprows, sheet_name=sheet_name)
        else:
            return pd.read_excel(ruta, skiprows=skiprows)
    else:
        raise ValueError("Formato de archivo no compatible")

ruta = "users/santi/Connections.csv"
nombre_user = ruta.split('/')[1]  # Esto divide la ruta y toma el segundo elemento después de dividir


connections = leer_archivo(f"users/{nombre_user}/Connections.csv", skiprows=3)
company_follows = leer_archivo(f"users/{nombre_user}/Company Follows.csv")
invitations = leer_archivo(f"users/{nombre_user}/Invitations.csv")
messages = leer_archivo(f"users/{nombre_user}/messages.csv")
publications = leer_archivo(f"users/{nombre_user}/contenido_mes.xlsx", sheet_name="PUBLICACIONES PRINCIPALES", skiprows=2)

print (nombre_user)


##Ahroa tenemos shares entonces esto cambia, hay que separar los compartidos de las publicaciones creadas

# Unificar las dos columnas 'Fecha de publicación' en una sola
# Buscar columnas vacías sin título
empty_columns = publications.columns[publications.isnull().all()]
print(empty_columns)

# Eliminar columnas vacías sin título
if not empty_columns.empty:
    publications = publications.drop(empty_columns, axis=1)
print(publications.columns)

# Renombrar las columnas primero
publications.columns = ['URL de publicación 1', 'Fecha de publicación 1', 'Interacciones ACACOLUMNAVACIA', 'URL de publicación 2', 'Fecha de publicación 2', 'Impresiones']

# Función para fusionar las dos columnas de fecha
def merge_dates(row):
    if pd.isnull(row['Fecha de publicación 1']):
        return row['Fecha de publicación 2']
    return row['Fecha de publicación 1']

# Aplicar la función para fusionar las fechas
publications['Fecha de publicación'] = publications.apply(merge_dates, axis=1)

# Eliminar las columnas de fecha individuales
publications.drop(['Fecha de publicación 1', 'Fecha de publicación 2'], axis=1, inplace=True)

#Preprocesamiento de columnas de fecha
print(publications.columns)

company_follows["Followed On"] = pd.to_datetime(company_follows["Followed On"]).dt.strftime("%m-%Y")
connections["Connected On"] = pd.to_datetime(connections["Connected On"]).dt.strftime("%m-%Y")
invitations["Sent At"] = pd.to_datetime(invitations["Sent At"]).dt.strftime("%m-%Y")
messages["DATE"] = pd.to_datetime(messages["DATE"]).dt.strftime("%m-%Y")
publications['Fecha de publicación'] = pd.to_datetime(publications['Fecha de publicación'])
publications['Fecha de publicación'] = publications['Fecha de publicación'].dt.strftime("%m-%Y")
# Renombra las columnas de fecha para uniformidad
company_follows.rename(columns={"Followed On": "month_year"}, inplace=True)
connections.rename(columns={"Connected On": "month_year"}, inplace=True)
invitations.rename(columns={"Sent At": "month_year"}, inplace=True)
messages.rename(columns={"DATE": "month_year"}, inplace=True)
publications.rename(columns={"Fecha de publicación": "month_year"}, inplace=True)

# Preprocesamiento de la columna 'Fecha de publicación' para asegurar que esté en formato datetime
# publications['month_year'] = pd.to_datetime(publications['month_year'], dayfirst=True)

# Hacer el conteo por fecha
conteo_publicaciones_por_fecha = publications.groupby('month_year').size().reset_index(name='Cantidad de Publicaciones')



### PRIMERO LEEMOS EL CSV DE CONNECTIONS 
#Cantidad total de contactos
contactos = len(connections)
print(f"Contactos: {contactos}")
# Agregados por dia
# Conteo de contactos por mes
conteo_contactos_por_mes = connections.groupby('month_year').size().reset_index(name='Cantidad de Contactos')

# Agregar conteo de contactos por mes al DataFrame df_final
for i in range(len(conteo_contactos_por_mes)):
    data_contactos = {
        'UserId': nombre_user,
        'InteraccionId': 8,  # Id correspondiente a la cantidad de contactos
        'Cantidad': conteo_contactos_por_mes.loc[i, 'Cantidad de Contactos'],
        'Fecha': conteo_contactos_por_mes.loc[i, 'month_year']
    }
    df_final.loc[len(df_final)] = data_contactos

## Leemos el CSV Company , visualizamos la cantidad de empresas diferentes que sigue cada user.
cant_empresas = 0

# Lista de empresas a excluir
empresas_excluidas = ["Kelsoft", "COSYS", "EducacionIT", "It School"]

# Filtrar las empresas seguidas excluyendo las específicas
empresas_no_excluidas = company_follows[~company_follows['Organization'].str.contains('|'.join(empresas_excluidas), flags=re.IGNORECASE)]

# Obtener el recuento de empresas seguidas por mes y año
empresas_por_mes = empresas_no_excluidas.groupby('month_year')['Organization'].nunique().reset_index()
empresas_por_mes.columns = ['month_year', 'Cantidad_empresas_seguidas']
for i in range(len(empresas_por_mes)):
    data = {
        'UserId': nombre_user,
        'InteraccionId': 3,
        'Cantidad': empresas_por_mes.loc[i, 'Cantidad_empresas_seguidas'],
        'Fecha': empresas_por_mes.loc[i, 'month_year']
    }
    # Agregar una nueva fila al DataFrame 'df_final' utilizando loc
    df_final.loc[len(df_final)] = data


#Aca tenemos las invitaciones envidas y recibidas y cuantas fueron con mensajes.
conteo_invitaciones = {}

invitaciones_totales = len(invitations)
for i in range(invitaciones_totales):
    direction = invitations.loc[i, 'Direction']
    year_month = invitations.loc[i, 'month_year']

    if year_month not in conteo_invitaciones:
        conteo_invitaciones[year_month] = {'enviadas': 0, 'recibidas': 0, 'mensajes_enviados': 0, 'mensajes_recibidos': 0}

    if invitations.loc[i, 'Message'] != '':
        if direction == 'OUTGOING':
            conteo_invitaciones[year_month]['mensajes_enviados'] += 1
        else:
            conteo_invitaciones[year_month]['mensajes_recibidos'] += 1

    if direction == 'OUTGOING':
        conteo_invitaciones[year_month]['enviadas'] += 1
    else:
        conteo_invitaciones[year_month]['recibidas'] += 1

    


for month_year, values in conteo_invitaciones.items():
    # Obtener los valores de las interacciones del diccionario
    invitaciones_recibidas = values['recibidas']
    invitaciones_enviadas = values['enviadas']
    mensajes_recibidos = values['mensajes_recibidos']
    mensajes_enviados = values['mensajes_enviados']

    # Registrar invitaciones recibidas
    data_inv_recibidas = {
        'UserId': nombre_user,
        'InteraccionId': 4,
        'Cantidad': invitaciones_recibidas,
        'Fecha': month_year
    }
    df_final.loc[len(df_final)] = data_inv_recibidas

    # Registrar invitaciones enviadas
    data_inv_enviadas = {
        'UserId': nombre_user,
        'InteraccionId': 5,
        'Cantidad': invitaciones_enviadas,
        'Fecha': month_year
    }
    df_final.loc[len(df_final)] = data_inv_enviadas

    # Registrar mensajes recibidos
    data_msg_recibidos = {
        'UserId': nombre_user,
        'InteraccionId': 6,
        'Cantidad': mensajes_recibidos,
        'Fecha': month_year
    }
    df_final.loc[len(df_final)] = data_msg_recibidos

    # Registrar mensajes enviados
    data_msg_enviados = {
        'UserId': nombre_user,
        'InteraccionId': 7,
        'Cantidad': mensajes_enviados,
        'Fecha': month_year
    }
    df_final.loc[len(df_final)] = data_msg_enviados

#

# Combina los DataFrames

# df_vs
# iteras cada uno de los df que tenes y vas cargando un registro por cada uno con el formato que necesitas para la base.
# 
for i in range(len(conteo_publicaciones_por_fecha)):
    data = {
        'UserId': nombre_user,
        'InteraccionId': 2,
        'Cantidad': conteo_publicaciones_por_fecha.loc[i, 'Cantidad de Publicaciones'] ,
        'Fecha': conteo_publicaciones_por_fecha.loc[i, 'month_year']
    }

    df_final.loc[len(df_final)] = data

st.write(df_final)
