import pandas as pd
from pandas import merge
import re

connections = pd.read_excel("More-20231129T191845Z-001/More/17-11/Connections.xlsx", skiprows=3)
company_follows = pd.read_excel("More-20231129T191845Z-001/More/17-11/Company Follows.xlsx")
content_month = pd.read_excel("More-20231129T191845Z-001/More/17-11/contenido del mes.xlsx")
invitations = pd.read_excel("More-20231129T191845Z-001/More/17-11/Invitations.xlsx")
messages = pd.read_excel("More-20231129T191845Z-001/More/17-11/messages.xlsx")

### PRIMERO LEEMOS EL CSV DE CONNECTIONS 
#Cantidad total de contactos
contactos = len(connections)
print(f"Contactos: {contactos}")
# Agregados por dia
conteo_por_fecha = connections.groupby('Connected On')['First Name'].count()

## Leemos el CSV Company , visualizamos la cantidad de empresas diferentes que sigue cada user.
cant_empresas = 0

def empresas_kelsoft(company_follows):
    empresas = []
    for i in company_follows["Organization"]:
        if re.search("(Kelsoft|COSYS|EducacionIT|It School)", i, re.IGNORECASE):
            empresas.append(i)
    return empresas

empresas_kelsoft = empresas_kelsoft(company_follows)

for i in company_follows["Organization"]:
    if i not in empresas_kelsoft:
        cant_empresas += 1

# # Filtramos el grupo Kelsoft
# filtro_netkel = "Grupo KELSOFT | NetKEL Consulting"
# filtro_cosys = "Cosys Global | Grupo KELSOFT"
# filtro_it = "EducacionIT"
# filtro_it2 = "It School - Educación IT | Grupo KELSOFT"
# # Aca ya tenemos la cantidad de empresas que sigue cada usuario
# for i in company_follows["Organization"]:
#     if i != filtro_netkel:
#         if i != filtro_cosys:
#             if i != filtro_it:
#                 if i != filtro_it2:
#                     cant_empresas += 1
print(f"Empresas seguidas (Excluyendo Grupo Kelsoft): {cant_empresas}")


#Aca tenemos las invitaciones envidas y recibidas y cuantas fueron con mensajes.
invitaciones_totales = len(invitations)
invitaciones_enviadas = 0
invitaciones_recibidas = 0
mensajes_enviados = 0
mensajes_recibidos = 0
for i in range(invitaciones_totales):
    if invitations["From"].loc[i] == invitations["From"].iloc[1]:
        invitaciones_enviadas += 1
    else:
        invitaciones_recibidas += 1
    if type(invitations["Message"].iloc[i]) != float:
        if invitations["From"].iloc[i] == invitations["From"].iloc[0]:
            mensajes_enviados += 1
        else:
            mensajes_recibidos += 1
print(f"Invitaciones Enviadas: {invitaciones_enviadas}")
print(f"Invitaciones Recibidas: {invitaciones_recibidas}")
print(f"Dando un total de: {invitaciones_totales}  invitaciones")
print(f"Invitaciones enviadas con mensaje: {mensajes_enviados}")
print(f"Invitaciones recibidas con mensaje: {mensajes_recibidos}")

# Preprocesamiento de columnas

connections_subset = connections[['First Name', 'First Name', 'URL','Connected On']]  # Reemplaza 'Columna3', 'Columna4', ... con los nombres de las columnas que necesitas
invitations_subset = invitations[['From', 'Sent At', 'Message']]  # Reemplaza 'Columna5', 'Columna6', ... con los nombres de las columnas que necesitas
messages_subset = messages[['CONVERSATION ID', 'FROM','TO','DATE']]  # Reemplaza 'Columna7', 'Columna8', ... con los nombres de las columnas que necesitas


# Preprocesamiento de columnas de fecha

company_follows["Followed On"] = pd.to_datetime(company_follows["Followed On"]).dt.strftime("%Y%m")
connections["Connected On"] = pd.to_datetime(connections["Connected On"]).dt.strftime("%Y%m")
invitations["Sent At"] = pd.to_datetime(invitations["Sent At"]).dt.strftime("%Y%m")
print(messages.columns)
messages["DATE"] = pd.to_datetime(messages["DATE"]).dt.strftime("%Y%m")

# Renombra las columnas de fecha para uniformidad
company_follows.rename(columns={"Followed On": "month_year"}, inplace=True)
connections.rename(columns={"Connected On": "month_year"}, inplace=True)
invitations.rename(columns={"Sent At": "month_year"}, inplace=True)
messages.rename(columns={"DATE": "month_year"}, inplace=True)

# Combina los DataFrames


# # ### PRIMERO LEEMOS EL CSV DE CONNECTIONS 
# # #Cantidad total de contactos
# # contactos = len(df)
# # # Agregados por dia
# # conteo_por_fecha = df.groupby('Connected On')['First Name'].count()
# # print(conteo_por_fecha)

data = {
    "User": "More",
    "Contactos": [contactos],
    "Cantidad empresas seguidas": [cant_empresas],
    "Invitaciones enviadas": [invitaciones_enviadas],
    "Invitaciones recibidas": [invitaciones_recibidas],
    "Mensajes en invitaciones enviadas": [mensajes_enviados],
    "Mensajes en invitaciones recibidas": [mensajes_recibidos],
    "Invitaciones totales": [invitaciones_totales]
}

# Convertir el diccionario a DataFrame
df_resumen = pd.DataFrame(data)

# Muestra el DataFrame

print(df_resumen)
