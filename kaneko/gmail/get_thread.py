import base64
import httplib2
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'secrets/junya.json'
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

if not threads:
    print('No threads found.')
else:
    print('id:', threads[0]['id'])
    thread = service.users().threads().get(userId='me', id=threads[0]['id']).execute()
    message = ''
    for part in thread['messages'][0]['payload']['parts']:
        message += base64.urlsafe_b64decode(part['body']['data']).decode()
    print(message)
