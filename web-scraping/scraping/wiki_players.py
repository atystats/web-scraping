from parsel import Selector
import requests 
import dateparser
import re

headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"}

def get_clubs_info(html):
    clubs = get_clubs(html)
    for c in clubs:
        if link := c.get('link'):
            response = requests.get(link, headers = headers)
            c['info'] = club_info(response.text)

    return clubs

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
            match = re.search('(?P<metric>[\d.]+.m) \((?P<imperial>(\d.ft.\d{1,2}.in))\)',value)
            if match is None:
                print('failed height match', value)
                continue
            # parts = value.split('(')
            # metric = parts[0].strip(' ').strip('\n')
            # imp = parts[1].strip(')')
            player_info['Height'] = {
                'imperial': match.group('imperial').replace('\u00a0', ' '),
                'metric': match.group('metric').replace('\u00a0', ' ')
            }
        elif key.startswith('Date of birth'):
            dob = tr.xpath("./td/text()[normalize-space()]").get()
            player_info['Date of birth'] = dob

    return player_info

def club_info(html):
    selector = Selector(text = html)
    trs = selector.xpath('//table[@class = "infobox vcard"]/tbody/tr')

    club_info = {}
    for tr in trs[1:]:
        key : str = tr.xpath("./th/text()").get()
        value = tr.xpath("./td/a/text()").get()
        if value is None:
            value = tr.xpath("./td/text()").get()
    
        if key is None:
            continue
        if key.startswith('Full name'):
            club_info["Full Name"] = value.strip('\n')
        elif key.startswith('Ground'):
            club_info['Ground'] = value
        elif key.startswith('Capacity'):
            club_info['Capacity'] = value
        elif key.startswith('Founded'):
            dat = tr.xpath("./td").get()
            match = re.search('(?P<Date>\d+\s\w+\s\d+)',dat)
            club_info['Founded'] = str(dateparser.parse(match.group('Date')))
            
    
    return club_info