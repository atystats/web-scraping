import requests
import json

#from bs_clubs import get_clubs
# from bs_select_clubs import get_clubs
from bs_xpath_clubs import get_clubs

#The header is mandatory for wikipedia. This has information on the Agent that is sending the request
headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"}

response = requests.get('https://en.wikipedia.org/wiki/Cristiano_Ronaldo', headers=headers)
new_list = get_clubs(response.text)

clubs_ronaldo = json.dumps(new_list)
print(clubs_ronaldo)

with open('Ronaldo_clubs.json', 'w', encoding='utf-8') as f:
    f.write(clubs_ronaldo)
