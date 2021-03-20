import os
import json
import random
from urllib.parse import urlencode
from urllib.request import urlopen

url = 'http://api.giphy.com/v1/gifs/search?'

def get_giphy():
    params = urlencode({
    'q': 'league of legends',
    'api_key': os.getenv('TOKEN_GIPHY'),
    'limit': '10'
    })

    with urlopen(f'{url}{params}') as response:
        data = json.loads(response.read())

    r = random.randrange(10)
    data = data.get('data', None)
    giphy = data[r]['url']
    return giphy