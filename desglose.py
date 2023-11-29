import pandas as pd
from pandas import merge


connections = pd.read_excel("More-20231129T191845Z-001/More/17-11/Connections.xlsx")
company_follows = pd.read_excel("More-20231129T191845Z-001/More/17-11/Company Follows.xlsx")
content_month = pd.read_excel("More-20231129T191845Z-001/More/17-11/contenido del mes.xlsx")
invitations = pd.read_excel("More-20231129T191845Z-001/More/17-11/Invitations.xlsx")
messages = pd.read_excel("More-20231129T191845Z-001/More/17-11/messages.xlsx")

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
