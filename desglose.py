import pandas as pd
from pandas import merge


connections = pd.read_excel("More-20231129T191845Z-001/More/17-11/Connections.xlsx")
company_follows = pd.read_excel("More-20231129T191845Z-001/More/17-11/Company Follows.xlsx")
content_month = pd.read_excel("More-20231129T191845Z-001/More/17-11/contenido del mes.xlsx")
invitations = pd.read_excel("More-20231129T191845Z-001/More/17-11/Invitations.xlsx")
messages = pd.read_excel("More-20231129T191845Z-001/More/17-11/messages.xlsx")

### PRIMERO LEEMOS EL CSV DE CONNECTIONS 
#Cantidad total de contactos
df_connections = pd.read_csv("Connections.csv")
contactos = len(df_connections)
print(f"Contactos: {contactos}")
# Agregados por dia
conteo_por_fecha = df_connections.groupby('Connected On')['First Name'].count()

## Leemos el CSV Company , visualizamos la cantidad de empresas diferentes que sigue cada user.
df_company = pd.read_csv("Company Follows.csv")
cant_empresas = 0
# Filtramos el grupo Kelsoft
filtro_netkel = "Grupo KELSOFT | NetKEL Consulting"
filtro_cosys = "Cosys Global | Grupo KELSOFT"
filtro_it = "EducacionIT"
filtro_it2 = "It School - Educación IT | Grupo KELSOFT"
# Aca ya tenemos la cantidad de empresas que sigue cada usuario
for i in df_company["Organization"]:
    if i != filtro_netkel:
        if i != filtro_cosys:
            if i != filtro_it:
                if i != filtro_it2:
                    cant_empresas += 1
print(f"Empresas seguidas (Excluyendo Grupo Kelsoft): {cant_empresas}")


## Leemos el CSV Invitations
df_invitations = pd.read_csv("Invitations.csv")
#Aca tenemos las invitaciones envidas y recibidas y cuantas fueron con mensajes.
invitaciones_totales = len(df_invitations)
invitaciones_enviadas = 0
invitaciones_recibidas = 0
mensajes_enviados = 0
mensajes_recibidos = 0
for i in range(invitaciones_totales):
    if df_invitations["From"].loc[i] == df_invitations["From"].iloc[1]:
        invitaciones_enviadas += 1
    else:
        invitaciones_recibidas += 1
    if type(df_invitations["Message"].iloc[i]) != float:
        if df_invitations["From"].iloc[i] == df_invitations["From"].iloc[0]:
            mensajes_enviados += 1
        else:
            mensajes_recibidos += 1
print(f"Invitaciones Enviadas: {invitaciones_enviadas}")
print(f"Invitaciones Recibidas: {invitaciones_recibidas}")
print(f"Dando un total de: {invitaciones_totales}  invitaciones")
print(f"Invitaciones enviadas con mensaje: {mensajes_enviados}")
print(f"Invitaciones recibidas con mensaje: {mensajes_recibidos}")

# Preprocesamiento de columnas de fecha
connections = connections.iloc[2:, :]

print(connections.head())

# company_follows["Followed On"] = pd.to_datetime(company_follows["Followed On"]).dt.strftime("%Y%m")
# connections["Connected On"] = pd.to_datetime(connections["Connected On"]).dt.strftime("%Y%m")
# invitations["Sent At"] = pd.to_datetime(invitations["Sent At"]).dt.strftime("%Y%m")
# messages["Date"] = pd.to_datetime(messages["Date"]).dt.strftime("%Y%m")

# # Renombra las columnas de fecha para uniformidad
# company_follows.rename(columns={"Followed On": "month_year"}, inplace=True)
# connections.rename(columns={"Connected On": "month_year"}, inplace=True)
# invitations.rename(columns={"Sent At": "month_year"}, inplace=True)
# messages.rename(columns={"Date": "month_year"}, inplace=True)

# # Combina los DataFrames
# df = merge(company_follows, connections, on="month_year")
# df = merge(df, invitations, on="month_year")
# df = merge(df, messages, on="month_year")


# print(df)
# # ### PRIMERO LEEMOS EL CSV DE CONNECTIONS 
# # #Cantidad total de contactos
# # contactos = len(df)
# # # Agregados por dia
# # conteo_por_fecha = df.groupby('Connected On')['First Name'].count()
# # print(conteo_por_fecha)
