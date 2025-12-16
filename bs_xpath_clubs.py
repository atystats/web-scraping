from parsel import Selector

def get_clubs(html):

    selector = Selector(text=html)
    matches = selector.xpath('//table[@class = "wikitable"]')[0] # '//' is used to find content in the whole document.
    trs = matches.xpath('.//tr')

    ronaldo_club = []
    club_links = []
    for tr in trs[2:]:
        clubs = tr.xpath('./td[1]')
        if not clubs:
            continue
        club = clubs.xpath("a/text()").get()
        if club is None:
            continue
        link = clubs.xpath("a/@href").get()
        club_link = f"https://en.wikipedia.org/{link}"
        ronaldo_club.append(club)
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