import gspread
import pandas as pd
import pymysql
from google_auth_oauthlib.flow import InstalledAppFlow
import numpy as np
import datetime

## Aca conectamos , mediante terminal, los csv a una base de datos, en este caso, un spreedsheet
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret_258260523243-d55smov40jlgkqdpar7lduol6ua4k81v.apps.googleusercontent.com.json", 
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
)
creds = flow.run_local_server(port=0)
client = gspread.authorize(creds)


#######
sheet = client.open_by_key("17Ge3iD3xswqericZ135yf33Jt8fqOg-55GZMw4IuQtk").worksheet("Datos")
data = sheet.get_all_values()
print(data)
