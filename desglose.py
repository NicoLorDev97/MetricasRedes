import pandas as pd

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

print(f"Contactos agregados por fecha: {conteo_por_fecha}")

# Tu código original para calcular las métricas
# Asegúrate de ejecutar esto primero

# Creación del DataFrame con las métricas
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

print(f"Contactos agregados por fecha: {conteo_por_fecha}")
