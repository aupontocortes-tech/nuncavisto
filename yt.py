import os, sys, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
# A chave vem da variável YT_TOKEN_JSON (Secret do GitHub). Nunca salve a chave no repositório.
c = Credentials.from_authorized_user_info(json.loads(os.environ['YT_TOKEN_JSON']))
if not c.valid: c.refresh(Request())
yt = build('youtube', 'v3', credentials=c)
if sys.argv[1] == 'me':
    r = yt.channels().list(part='snippet', mine=True).execute(); print([(i['id'], i['snippet']['title']) for i in r.get('items', [])])
elif sys.argv[1] == 'up':
    m = json.load(open(sys.argv[3], encoding='utf-8'))
    # trava de segurança: só publica no canal Nunca Visto
    me = yt.channels().list(part='snippet', mine=True).execute()['items'][0]
    if me['id'] != 'UCIKnhxWJaxbmCudg2Qp9YhA': sys.exit('ERRO: a chave não é do canal Nunca Visto (' + me['snippet']['title'] + ')')
    body = {'snippet': {'title': m['title'], 'description': m['description'], 'tags': m.get('tags', []), 'categoryId': '28',
                        'defaultLanguage': 'pt-BR', 'defaultAudioLanguage': 'pt-BR'},
            'status': {'privacyStatus': m.get('privacy', 'public'), 'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': False}}
    r = yt.videos().insert(part='snippet,status', body=body, media_body=MediaFileUpload(sys.argv[2], chunksize=-1, resumable=True)).execute()
    print(r['id'], r['status'])
