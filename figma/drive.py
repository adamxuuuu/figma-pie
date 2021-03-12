from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from pathlib import Path

HOME = Path(__file__).parents[1]

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1GQc_QEqIe9rW37UL7QB9YBnZ_-2kjhVukxM0JyRSor8'
RANGE_NAME = 'Attributes!D2:G'


def __credential():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    token_path = HOME / 'secret/token.pickle'
    if token_path.exists():
        creds = pickle.loads(token_path.read_bytes())

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                HOME / 'secret/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        (HOME / 'secret/token.pickle').write_bytes(pickle.dumps(creds))
    return creds


def updateSheet(sheet_id=SPREADSHEET_ID, range_name=RANGE_NAME):
    """
    Update a range of cells within a specified spread sheet
    :param sheet_id: Spread sheet to update
    :param range_name: Cells to select
    """
    # Get credential
    creds = __credential()

    # Establish connection
    service = build('sheets', 'v4', credentials=creds)

    # Get data
    raw = (HOME / 'attributes.txt').read_text(encoding='utf-8').split('\n')

    body = {'values': [d.split('|') for d in raw]}

    # Call the Sheets API
    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    print('-> {0} cells updated'.format(result.get('updatedCells')))
