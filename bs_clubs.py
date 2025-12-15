from bs4 import BeautifulSoup

def get_clubs(html):

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', attrs= {'class': "wikitable"}) # a are called anchor used to represent hyperlinks.

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


    new_list = []
    for item in ronaldo_club:
        s_item = str(item)
        if not any (char.isdigit() for char in s_item):
            new_list.append(item.strip('\n'))

    return new_list