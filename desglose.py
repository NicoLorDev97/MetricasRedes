import pandas as pd
from pandas import merge
import re
import streamlit as st
import matplotlib.pyplot as plt


connections = pd.read_excel("More-20231129T191845Z-001/More/17-11/Connections.xlsx", skiprows=3)
company_follows = pd.read_excel("More-20231129T191845Z-001/More/17-11/Company Follows.xlsx")
content_month = pd.read_excel("More-20231129T191845Z-001/More/17-11/contenido del mes.xlsx")
invitations = pd.read_excel("More-20231129T191845Z-001/More/17-11/Invitations.xlsx")
messages = pd.read_excel("More-20231129T191845Z-001/More/17-11/messages.xlsx")
publications = pd.read_excel("More-20231129T191845Z-001/More/17-11/contenido del mes.xlsx", sheet_name="PUBLICACIONES PRINCIPALES", skiprows=2)

# Unificar las dos columnas 'Fecha de publicación' en una sola
#Antes es necesario renombrarlas porque los nombres estan repetidos
# publications.columns = ['URL de publicación 1', 'Fecha de publicación 1', 'Interacciones', 'URL de publicación 2', 'Fecha de publicación 2', 'Impresiones']
# publications['Fecha de publicación'] = pd.concat([publications['Fecha de publicación'], publications['Fecha de publicación']]).dropna()

# # Preprocesamiento de la columna 'Fecha de publicación' para asegurar que esté en formato datetime
# publications['Fecha de publicación'] = pd.to_datetime(publications['Fecha de publicación'], dayfirst=True)
# conteo_publicaciones_por_fecha = publications.groupby('Fecha de publicación').size().reset_index(name='Cantidad de Publicaciones')

# st.title("conteo de publicaciones por fecha")

# st.write(conteo_publicaciones_por_fecha)


#Preprocesamiento de columnas de fecha
print(publications.columns)
company_follows["Followed On"] = pd.to_datetime(company_follows["Followed On"]).dt.strftime("%Y%m")
connections["Connected On"] = pd.to_datetime(connections["Connected On"]).dt.strftime("%Y%m")
invitations["Sent At"] = pd.to_datetime(invitations["Sent At"]).dt.strftime("%Y%m")
messages["DATE"] = pd.to_datetime(messages["DATE"]).dt.strftime("%Y%m")

# Renombra las columnas de fecha para uniformidad
company_follows.rename(columns={"Followed On": "month_year"}, inplace=True)
connections.rename(columns={"Connected On": "month_year"}, inplace=True)
invitations.rename(columns={"Sent At": "month_year"}, inplace=True)
messages.rename(columns={"DATE": "month_year"}, inplace=True)

### PRIMERO LEEMOS EL CSV DE CONNECTIONS 
#Cantidad total de contactos
contactos = len(connections)
print(f"Contactos: {contactos}")
# Agregados por dia
conteo_por_fecha = connections.groupby('month_year')['First Name'].count()

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

#

# Combina los DataFrames
print(company_follows)


data = {
    "User": "More",
    "Contactos": [contactos],
    # "Contactos por fecha":
    "Cantidad empresas seguidas": [cant_empresas],
    "Invitaciones enviadas": [invitaciones_enviadas],
    "Invitaciones recibidas": [invitaciones_recibidas],
    "Mensajes en invitaciones enviadas": [mensajes_enviados],
    "Mensajes en invitaciones recibidas": [mensajes_recibidos],
    "Invitaciones totales": [invitaciones_totales]
}

# Convertir el diccionario a DataFrame
df_resumen = pd.DataFrame(data)

# # Muestra el DataFrame

# connections_dict = connections.groupby('month_year').apply(lambda x: x.to_dict(orient='records')).to_dict()
# company_follows_dict = company_follows.groupby('month_year').apply(lambda x: x.to_dict(orient='records')).to_dict()
# invitations_dict = invitations.groupby('month_year').apply(lambda x: x.to_dict(orient='records')).to_dict()
# messages_dict = messages.groupby('month_year').apply(lambda x: x.to_dict(orient='records')).to_dict()
# fecha_especifica = '202311'  # Cambia esto por la fecha que desees buscar
# datos_connections = connections_dict.get(fecha_especifica, [])

# df_resumen = pd.DataFrame(data)

st.title("Resumen de datos")
st.write("Datos recopilados:")

# Mostrar el DataFrame generado a partir del diccionario data
st.write(df_resumen)

st.title("Conteo de conexiones por mes y año")
st.write("Datos de conexiones por mes y año:")

# Mostrar el DataFrame generado a partir del conteo de conexiones por día
st.write(conteo_por_fecha)


# Gráfico de barras para invitaciones enviadas y recibidas
fig, ax = plt.subplots()
ax.bar(['Enviadas', 'Recibidas'], [invitaciones_enviadas, invitaciones_recibidas])
ax.set_title('Cantidad de invitaciones')
ax.set_ylabel('Cantidad')
st.pyplot(fig)

