from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
import pandas as pd


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8899)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
# get list of emails/messages matching the query
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="subject: ARK Investment Management Trading Information").execute()
    messages = results.get("messages", [])

    msg = service.users().messages().get(userId="me", id=messages[0]["id"], format="full").execute()# access the content of the message
    msg_data = msg["payload"]["body"]["data"] # bytes# decode bytes to html
    msg_html = base64.urlsafe_b64decode(msg_data).decode()
    
    msg = service.users().messages().get(userId="me", id=messages[0]["id"], format="full").execute()# access the content of the message
    msg_data = msg["payload"]["body"]["data"] # bytes# decode bytes to html
    msg_html = base64.urlsafe_b64decode(msg_data).decode()

    df = pd.read_html(msg_html, header=0, index_col=0)[0]
    print(df)
    
#     if not labels:
#         print('No labels found.')
#     else:
#         print('Labels:')
#         for label in labels:
#             print(label['name'])
            
    return df

if __name__ == '__main__':
    ark_daily_trades = main()
    
ark_daily_trades.to_pickle('data_pickle/ark_daily_trades') # Update path