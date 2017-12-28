from bs4 import BeautifulSoup
from pyjarowinkler import distance
import string
import httplib2
import re

band_label_pattern = re.compile(r'\(([A-Za-z]*\s+)?[Bb]and\)')
http = httplib2.Http()
band_lists = [
    "https://en.wikipedia.org/wiki/List_of_progressive_metal_artists",
    "https://en.wikipedia.org/wiki/List_of_deathcore_artists",
    "https://en.wikipedia.org/wiki/List_of_metalcore_bands"
]
with open('artists.txt','r') as artistfile:
    artists = set([line.strip() for line in artistfile.readlines()])


def get_artists(url):
    global artists
    try:
        status, response = http.request(url)
        soup = BeautifulSoup(response,'lxml')
        if status['status'] != '200':
            print("Status Code of %s received." % status['status'])

        if ('metalcore' in url):
            table = soup.find("table", {"class":"wikitable"})
            elements = table.find_all('td')

        if ('deathcore' in url or 'progressive' in url):
            table = soup.find("div",class_="div-col")
            elements = table.find_all('li')

        for element in elements:
            if (element.find('a')):
                title = (element.find('a').get('title'))
                title = band_label_pattern.sub('', title).strip()
                title = title.translate(None, string.punctuation)
                artists.add(title)

    except Exception as e:
        print(e)


for band_list in band_lists:
    get_artists(band_list)
print(len(artists),artists)

with open('artists.txt','w') as artistfile:
    for artist in artists:
        try:
            artistfile.write(artist + '\n')
        except:
            print("Couldn't write artist: %s. Skipping..." % artist)