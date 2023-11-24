from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd

## Aca conectamos , mediante terminal, los csv a una base de datos, en este caso, un spreedsheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret_258260523243-d55smov40jlgkqdpar7lduol6ua4k81v.apps.googleusercontent.com.json.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('sheets', 'v4', credentials=creds)