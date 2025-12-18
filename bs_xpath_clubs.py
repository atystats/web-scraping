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

def get_player_info(html):
    selector = Selector(text = html)
    trs = selector.xpath('//table[@class = "infobox infobox-table vcard"]/tbody/tr')

    player_info = {
        'name': None,
        'image': None
    }
    
    player_info['name'] = selector.xpath('//table[@class = "infobox infobox-table vcard"]/caption/text()').get()
    link = trs[0].xpath('./td/span/a/@href').get()
    player_info['image'] = f"https://en.wikipedia.org/{link}"
    
    for tr in trs[2:]:
        key : str = tr.xpath("./th/text()").get()
        value = tr.xpath("./td/a/text()").get()
        if value is None:
            value = tr.xpath("./td/text()").get()

        if key is None or value is None:
            continue

        if key.startswith('Full name'):
            player_info["Full Name"] = value.strip('\n')
        elif key.startswith('Place of birth'):
            player_info['Birth Place'] = value
        elif key.startswith('Height'):
            parts = value.split('(')
            metric = parts[0].strip(' ')
            imp = parts[1].strip(')')
            player_info['Height'] = {
                'imperial': imp,
                'metric': metric
            }

    return player_info

