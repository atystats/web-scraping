import requests
from bs4 import BeautifulSoup
import json

#The header is mandatory for wikipedia. This has information on the Agent that is sending the request
headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"}

response = requests.get('https://en.wikipedia.org/wiki/Cristiano_Ronaldo', headers=headers)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title)
print(soup.title.string)
tables = soup.find_all('table', attrs= {'class': "wikitable"}) # a are called anchor used to represent hyperlinks.
# print(len(tables))
#print(tables[0])
matches = tables[0]
trs = matches.find_all('tr')
ronaldo_club = []
for tr in trs:
    tds = tr.find_all('td')
    if not tds:
        continue
    clubs = tds[0]
    if clubs.a is None:
        ronaldo_club.append(clubs.get_text())
        continue
    club_name = clubs.a.string
    ronaldo_club.append(club_name)
    # if club_name is not None:
    #     ronaldo_club.append(club_name)
    #     continue

    # club_name = clubs.a.string
    # ronaldo_club.append(club_name)
    # if clubs is None:
    #     continue
    # club_name = clubs.a.string
    # ronaldo_club.append(club_name)

new_list = []
for item in ronaldo_club:
    s_item = str(item)
    if not any (char.isdigit() for char in s_item):
        new_list.append(item.strip('\n'))
print(new_list)
clubs_ronaldo = json.dumps(new_list)
print(clubs_ronaldo)
#print(trs)
## Html tags also contain attributes so we can also filter on attributes
# response.raise_for_status()
 #If this is 200, the parsing is successful.
# print(response.text)





with open('Ronaldo_clubs.json', 'w', encoding='utf-8') as f:
    f.write(clubs_ronaldo)


# with open('Brian.html', 'r', encoding='utf-8') as f:
#     contents = f.read()
#     print(contents)
