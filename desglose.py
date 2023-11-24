import pandas as pd

df = pd.read_csv("Connections.csv")
### PRIMERO LEEMOS EL CSV DE CONNECTIONS 
#Cantidad total de contactos
contactos = len(df)
# Agregados por dia
conteo_por_fecha = df.groupby('Connected On')['First Name'].count()
print(conteo_por_fecha)
