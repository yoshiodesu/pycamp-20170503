import base64
import httplib2
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

__author__ = 'Yoshio <msokbp@yahoo.co.jp>'

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'secrets/client_id.json'
APPLICATION_NAME = 'pycamp-20170503'

store = Storage('secrets/gmail.json')
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    credentials = tools.run_flow(flow, store)

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

results = service.users().threads().list(userId='me').execute()
threads = results.get('threads', [])

number_read_massage=range(2)
n_thread=0
n_message=0
for var in number_read_massage:
    n_thread += 0
    n_message +=1
    if not threads:
        print('No threads found.')
    else:
        print('id:', threads[n_thread]['id'])
        thread = service.users().threads().get(userId='me', id=threads[n_thread]['id']).execute()
        message = ''
        for part in thread['messages'][n_thread]['payload']['parts']:
            message += base64.urlsafe_b64decode(part['body']['data']).decode()
    print(n_thread)
    print(message[0:100])
    print("")
