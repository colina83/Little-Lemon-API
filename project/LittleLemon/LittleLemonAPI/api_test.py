import requests
from requests.auth import HTTPBasicAuth
import json

url = 'https://colina83-reimagined-chainsaw-wr9jwvqr9v9cgw5w-8000.preview.app.github.dev/api/manager/'
username = 'john83'
token = '829c5f743ef7f23f76768a1e511b5e43573eb64d'

response = requests.get(url, auth=HTTPBasicAuth(username, token))
data = response.json()

print(json.dumps(data, indent=4))