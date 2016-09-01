from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import base64

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class Connector(object):

  CLIENT_SECRET_FILE = 'client_secret.json'
  APPLICATION_NAME = 'Google Sheets API Python Quickstart'

  def get_credentials(self):
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,self.CRED_FILE_NAME)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
        flow.user_agent = self.APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
class Spreadsheet(Connector):

  SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
  CRED_FILE_NAME='sheets.googleapis.com-python-quickstart.json'

  def getService(self):
    credentials = self.get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    self.service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    return

  def getData(self,spreadsheetId,rangeName):
    result = self.service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    return result.get('values', [])

class Gmail(Connector):

  SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
  CRED_FILE_NAME='gmail-python-quickstart.json'

  def getService(self):
    credentials = self.get_credentials()
    http = credentials.authorize(httplib2.Http())
    #TODO: check v4 and check w/o disciverURL
    self.service = discovery.build('gmail', 'v1', http=http)
    return

  def getData(self,user):
    results = self.service.users().messages().list(userId='me',q='from:%s || to:%s' %(user,user)).execute()
    return results.get('messages', [])

  def getMessage(self,msg_id):
    return self.service.users().messages().get(userId='me', id=msg_id,
                                             format='full').execute()

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    
    sheet = Spreadsheet()
    sheet.getService()

    spreadsheetId = '1DIVDeyJYxf_rdhHFvxhPTrhWli1ljh_2M1tnN5X1Lqg'
    rangeName = 'A1:I14'
    values = sheet.getData(spreadsheetId,rangeName)

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))
    """
    gmail = Gmail()
    gmail.getService()
    labels = gmail.getData('no-reply@accounts.google.com')

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        msg = gmail.getMessage(label['id'])
#        print(msg)
#        print(base64.b64decode(msg['payload']['body'][:-3]))
        for part in msg['payload']['parts']:
          print (base64.b64decode(part['body']['data'][:-1]))
#        for key in msg['payload']:
#          print(key)
        exit()


if __name__ == '__main__':
    main()
