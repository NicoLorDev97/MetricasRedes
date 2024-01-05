import pandas as pd
import os
import re
import datetime

#df_final= pd.DataFrame(columns=['UserId', 'InteraccionId', 'Cantidad', 'Fecha'])

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

def Connections(nombre_user,df_final,inicio):
    connections = leer_archivo(f"users/{nombre_user}/Connections.csv", skiprows=3)
    connections["Connected On"] = pd.to_datetime(connections["Connected On"]).dt.strftime("%m-%Y")
    connections.rename(columns={"Connected On": "month_year"}, inplace=True)
    conteo_contactos_por_mes = connections.groupby('month_year').size().reset_index(name='Cantidad de Contactos')
    fecha_inicio = datetime.datetime.strptime(inicio, "%d/%m/%Y")
    fecha_inicio = fecha_inicio.strftime("%m-%Y")
    print(fecha_inicio)
    for i in range(len(conteo_contactos_por_mes)):
        fecha_actual = conteo_contactos_por_mes["month_year"].iloc[i]
        if fecha_actual >= fecha_inicio:
            data_contactos = {
                'UserId': nombre_user,
                'InteraccionId': 8,  # Id correspondiente a la cantidad de contactos
                'Cantidad': conteo_contactos_por_mes.loc[i, 'Cantidad de Contactos'],
                'Fecha': conteo_contactos_por_mes.loc[i, 'month_year']
            }
            df_final.loc[len(df_final)] = data_contactos
    return df_final

def Empresas_seguidas(nombre_user,df_final,inicio):
    company_follows = leer_archivo(f"users/{nombre_user}/Company Follows.csv")
    company_follows["Followed On"] = pd.to_datetime(company_follows["Followed On"]).dt.strftime("%m-%Y")
    company_follows.rename(columns={"Followed On": "month_year"}, inplace=True)
    #cant_empresas = 0
    empresas_excluidas = ["Kelsoft", "COSYS", "EducacionIT", "It School"]
    empresas_no_excluidas = company_follows[~company_follows['Organization'].str.contains('|'.join(empresas_excluidas), flags=re.IGNORECASE)]
    empresas_por_mes = empresas_no_excluidas.groupby('month_year')['Organization'].nunique().reset_index()
    empresas_por_mes.columns = ['month_year', 'Cantidad_empresas_seguidas']
    fecha_inicio = datetime.datetime.strptime(inicio, "%d/%m/%Y")
    fecha_inicio = fecha_inicio.strftime("%m-%Y")
    for i in range(len(empresas_por_mes)):
        fecha_actual = empresas_por_mes["month_year"].iloc[i]
        if fecha_actual >= fecha_inicio:
            data = {
                'UserId': nombre_user,
                'InteraccionId': 3,
                'Cantidad': empresas_por_mes.loc[i, 'Cantidad_empresas_seguidas'],
                'Fecha': empresas_por_mes.loc[i, 'month_year']
            }
            # Agregar una nueva fila al DataFrame 'df_final' utilizando loc
            df_final.loc[len(df_final)] = data
    return df_final

def Invitaciones(nombre_user,df_final,inicio):
    invitations = leer_archivo(f"users/{nombre_user}/Invitations.csv")
    invitations["Sent At"] = pd.to_datetime(invitations["Sent At"]).dt.strftime("%m-%Y")
    invitations.rename(columns={"Sent At": "month_year"}, inplace=True)
    conteo_invitaciones = {}
    invitaciones_totales = len(invitations)
    fecha_inicio = datetime.datetime.strptime(inicio, "%d/%m/%Y")
    fecha_inicio = fecha_inicio.strftime("%m-%Y")
    for i in range(invitaciones_totales):
        direction = invitations.loc[i, 'Direction']
        year_month = invitations.loc[i, 'month_year']
        fecha_actual = invitations["month_year"].iloc[i]
        if fecha_actual >= fecha_inicio:
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
    #print(df_final)
    return df_final

def Publicaciones(nombre_user,df_final,inicio):
    shares = leer_archivo(f"users/{nombre_user}/Shares.csv")
    columnas_a_eliminar = ['SharedURL', 'MediaURL', 'Visibility']
    shares = shares.drop(columnas_a_eliminar, axis=1)
    shares["Date"] = pd.to_datetime(shares["Date"]).dt.strftime("%m-%Y")
    shares.rename(columns={"Date": "month_year"}, inplace=True)
    shares.groupby("month_year")
    fecha_inicio = datetime.datetime.strptime(inicio, "%d/%m/%Y")
    fecha_inicio = fecha_inicio.strftime("%m-%Y")
    for i in range(len(shares)):
        fecha_actual = shares["month_year"].iloc[i]
        if fecha_actual >= fecha_inicio:
            if pd.isnull(shares["ShareCommentary"].iloc[i]):
                data = {
                        'UserId': nombre_user,
                        'InteraccionId': 12,
                        'Cantidad': 1,
                        'Fecha': shares["month_year"].iloc[i]
                    }
                df_final.loc[len(df_final)] = data
                df_final = df_final.groupby(['UserId', 'InteraccionId', 'Fecha'], as_index=False)['Cantidad'].sum()
            else:
                data = {
                        'UserId': nombre_user,
                        'InteraccionId': 2,
                        'Cantidad': 1,
                        'Fecha': shares["month_year"].iloc[i]
                    }
                df_final.loc[len(df_final)] = data
                df_final = df_final.groupby(['UserId', 'InteraccionId', 'Fecha'], as_index=False)['Cantidad'].sum()
    #print(df_final)
    return df_final

def Reacciones(nombre_user,df_final,inicio):
    reactions = leer_archivo(f"users/{nombre_user}/Reactions.csv")
    columnas_a_eliminar = ['Link']
    reactions = reactions.drop(columnas_a_eliminar, axis=1)
    reactions["Date"] = pd.to_datetime(reactions["Date"]).dt.strftime("%m-%Y")
    reactions.rename(columns={"Date": "month_year"}, inplace=True)
    fecha_inicio = datetime.datetime.strptime(inicio, "%d/%m/%Y")
    fecha_inicio = fecha_inicio.strftime("%m-%Y")
    for i in range(len(reactions)):
        fecha_actual = reactions["month_year"].iloc[i]
        if fecha_actual >= fecha_inicio:
            data = {
                        'UserId': nombre_user,
                        'InteraccionId': 11,
                        'Cantidad': 1,
                        'Fecha': reactions["month_year"].iloc[i]
                        }
            df_final.loc[len(df_final)] = data
            df_final = df_final.groupby(['UserId', 'InteraccionId', 'Fecha'], as_index=False)['Cantidad'].sum()
    return df_final

def Inbox(nombre_user,df_final,inicio):   
    messages = leer_archivo(f"users/{nombre_user}/messages.csv")
    columnas_a_eliminar = ['CONVERSATION ID', 'CONVERSATION TITLE', 'SENDER PROFILE URL','RECIPIENT PROFILE URLS', 'SUBJECT', 'CONTENT']
    messages = messages.drop(columnas_a_eliminar, axis=1)
    messages["DATE"] = pd.to_datetime(messages["DATE"]).dt.strftime("%m-%Y")
    messages.rename(columns={"DATE": "month_year"}, inplace=True)
    fecha_inicio = datetime.datetime.strptime(inicio, "%d/%m/%Y")
    fecha_inicio = fecha_inicio.strftime("%m-%Y")
    for i in range(len(messages)):
        fecha_actual = messages["month_year"].iloc[i]
        if fecha_actual >= fecha_inicio:
            if nombre_user == messages["FROM"].iloc[i]:
                data = {
                        'UserId': nombre_user,
                        'InteraccionId': 9,
                        'Cantidad': 1,
                        'Fecha': messages["month_year"].iloc[i]
                        }
                df_final.loc[len(df_final)] = data
                df_final = df_final.groupby(['UserId', 'InteraccionId', 'Fecha'], as_index=False)['Cantidad'].sum()
            else:
                data = {
                        'UserId': nombre_user,
                        'InteraccionId': 10,
                        'Cantidad': 1,
                        'Fecha': messages["month_year"].iloc[i]
                        }
                df_final.loc[len(df_final)] = data
                df_final = df_final.groupby(['UserId', 'InteraccionId', 'Fecha'], as_index=False)['Cantidad'].sum()
    return df_final

def Comentarios(nombre_user,df_final,inicio):
    comments = leer_archivo(f"users/{nombre_user}/Comments.csv")
    columnas_a_eliminar = ["Message","Link"]
    comments = comments.drop(columnas_a_eliminar, axis=1)
    comments['Date'] = pd.to_datetime(comments['Date'], errors='coerce')
    comments = comments.dropna(subset=['Date'])
    comments = comments[~(comments['Date'].isnull() & comments.astype(str).apply(lambda row: "Suerte en la busqueda!" in row.values, axis=1))]
    comments.reset_index(drop=True, inplace=True)
    comments["Date"] = pd.to_datetime(comments["Date"]).dt.strftime("%m-%Y")
    comments.rename(columns={"Date": "month_year"}, inplace=True)
    fecha_inicio = datetime.datetime.strptime(inicio, "%d/%m/%Y")
    fecha_inicio = fecha_inicio.strftime("%m-%Y")
    for i in range(len(comments)):
        fecha_actual = comments["month_year"].iloc[i]
        if fecha_actual >= fecha_inicio:
            data = {
                'UserId': nombre_user,
                'InteraccionId': 12,
                'Cantidad': 1,
                'Fecha': comments["month_year"].iloc[i]
                }
            df_final.loc[len(df_final)] = data
            df_final = df_final.groupby(['UserId', 'InteraccionId', 'Fecha'], as_index=False)['Cantidad'].sum()
    return df_final

