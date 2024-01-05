import pandas as pd
import desglose as d
import funciones as f


spreadsheet_key = "17Ge3iD3xswqericZ135yf33Jt8fqOg-55GZMw4IuQtk" #Aca definimos la ID de la base de datos, que sera siempre la misma ya que es la base.
direct = "C:/Users/nicol/OneDrive/Escritorio/Metricas/users"
usuarios = f.ObtenerUsers(direct)
df_final= pd.DataFrame(columns=['UserId', 'InteraccionId', 'Cantidad', 'Fecha'])
data_inicio = f.ObtenerInicios(spreadsheet_key)
for user in usuarios:
    df_aux = pd.DataFrame(columns=['UserId', 'InteraccionId', 'Cantidad', 'Fecha'])
    inicio = f.ObtenerInicio(data_inicio,user)
    df_aux = f.ObtenerDF(user,df_aux,inicio)
    df_final = pd.concat([df_final, df_aux], ignore_index=True)

worksheet_name = "Interacciones"
worksheet = f.ConexionCarga(spreadsheet_key,worksheet_name)
f.Carga(worksheet,df_final)
