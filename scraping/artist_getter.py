from bs4 import BeautifulSoup
from pyjarowinkler import distance
import httplib2
import re

http = httplib2.Http()
base_list_url = "https://en.wikipedia.org/wiki/List_of_heavy_metal_bands"
artists = [line.strip() for line in open('artists.txt','r').readlines()]
recur_limit = 3

def get_artists(url):
    try:
        status, response = http.request(url)
        soup = BeautifulSoup(response,'lxml')
        if status['status'] != '200':
            print("Status Code of %s received." % status['status'])

        elements = soup.find_all("div", {"class":"wikitable"})
        for element in elements:
            print(element.text)


    except Exception as e:
        print e

get_artists(base_list_url)