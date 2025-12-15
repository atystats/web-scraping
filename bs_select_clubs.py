from bs4 import BeautifulSoup

def get_clubs(html):

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.select('table[class = "wikitable"]') # select is used to find content using css selectors
    matches = tables[0]
    trs = matches.select('tr')
    ronaldo_club = []
    club_links =[]
    for tr in trs:
        clubs = tr.select_one('td:nth-child(1)')
        club_link = None
        if not clubs:
            continue
        club = clubs.select_one("a")
        if club is None:
            continue
        club_link = f"https://en.wikipedia.org/{club['href']}"
        ronaldo_club.append(club.string)
        club_links.append(club_link)

    new_list = []
    for index, item in enumerate(ronaldo_club):
        club_dict = {}
        s_item = str(item)
        if not any (char.isdigit() for char in s_item):
            club_dict["name"] = item.strip('\n')
            club_dict["link"] = club_links[index]
            new_list.append(club_dict)
            

    return new_list