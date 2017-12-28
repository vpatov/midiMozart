from bs4 import BeautifulSoup
import re

url_pattern = re.compile(r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')

song_reg = re.compile(r'\(ver \d+\)')
int_reg = re.compile(r'\d+')

#tab_download_link = 'https://tabs.ultimate-guitar.com/tabs/download?id=972187&session_id=8d03d867b49af197aa41ef3a71f76daa'

def tab_download_link(id):
    return 'https://tabs.ultimate-guitar.com/tabs/download?id=' + \
    str(id) + '&session_id=1234abcdef'

def get_tab_download_page_links(artist_source):
    url_dict = {}

    soup = BeautifulSoup(artist_source,'lxml')
    body = soup.find('body')
    tbodies = body.findAll('table')
    largest_tbody = tbodies[0]
    for tbody in tbodies:
        if len(tbody) > len(largest_tbody):
            largest_tbody = tbody

    for tr in largest_tbody.findAll('tr'):
        trs = tr.findAll('td')
        if (trs):
            typeoftab = trs[-1].text
        else:
            continue
        if (typeoftab.strip() != 'Guitar Pro'):
            continue

        ###TODO filter out the same songs that end with (ver 2) and (ver 3)... and take the  best one
        ###TODO replace findAll('tbody') with ('table') when doing from http response

        rating_td = tr.find('span',{'class':'rating'})
        if (not rating_td):
            continue
        rating_count = tr.find('font',{'class':'upc'})
        if (not rating_count):
            continue
        rating_count = int(rating_count.text)
        link = tr.find('a').get('href')
        song_name_text = tr.find('a').text
        song_ver = 1
        song_name = song_name_text

        m = song_reg.search(song_name_text)


        if (m):
            song_name = song_name_text[:m.start()].strip()

            song_ver = int(int_reg.search(song_name_text[m.start():]).group())

        rating_val = float(rating_td['title'])


        if rating_val >= 4.0:
            if song_name in url_dict:
                url_dict[song_name].append((rating_count,rating_val,song_ver,link))
            else:
                url_dict[song_name] = [(rating_count,rating_val,song_ver,link)]


    urls = []
    for song_name in url_dict:
        link = max(url_dict[song_name])[3]
        urls.append((link,song_name))
    return urls

def get_tab_download_link(tab_source):
    try:
        soup = BeautifulSoup(tab_source, 'lxml')
        div = soup.find('div',{'class':'textversbox'})
        id = div.find('input',{'id':'tab_id'})
        return tab_download_link(id.get('value'))
    except Exception as e:
        print(e)
    return 'broken'

