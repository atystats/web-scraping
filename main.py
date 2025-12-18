import requests
import json
import sys

#from bs_clubs import get_clubs
# from bs_select_clubs import get_clubs
from bs_xpath_clubs import get_clubs, get_player_info

#The header is mandatory for wikipedia. This has information on the Agent that is sending the request
headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"}


if len(sys.argv) == 1:
    raise Exception("missing argument...")

target = sys.argv[1]
url = sys.argv[2]
output = sys.argv[3]

handler = None
if target == 'club':
    handler = get_clubs
elif target == 'info':
    handler = get_player_info

response = requests.get(url, headers=headers)
results = handler(response.text)

results = json.dumps(results)

with open(f'{output}.json', 'w', encoding='utf-8') as f:
    f.write(results)
