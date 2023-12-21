import os


def ObtenerUsers(directorio):
    directorio_data = directorio
    archivos = os.listdir(directorio_data)
    users = archivos
    return users

ObtenerUsers("C:/Users/nicol/OneDrive/Escritorio/Metricas/Data")