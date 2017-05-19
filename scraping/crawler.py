import httplib2
import time
from selenium import webdriver
import scraper
import selenium.webdriver.chrome.service as service


http = httplib2.Http()
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'

base_url = "https://www.ultimate-guitar.com"
search_suffix = "/search.php?search_type=title&order=&value="


artists = [i.strip() for i in open('artists.txt','r').read().split('\n')]


def artist_url(band_name,page_num):
    return base_url + '/tabs/' + band_name.strip().replace(' ','_') + '_tabs' + str(page_num) + '.htm'


#
# status,response = http.request(artist_url('All That Remains',1))



tab_links = []
response = open('all_that_remains_tabs.htm','r').read()
tab_links += scraper.get_song_urls(response)


exit()
tab_links = []
tab_file = open('tab_links.txt','w')
for artist in artists:
    page_num = 0
    while (True):
        status, response = http.request(artist_url(artist,page_num))
        if (len(response) < 8000):
            break
        tab_links += scraper.get_song_urls(response)
        for tab in tab_links:
            tab_file.write(tab[0] +',' + tab[1] + '\n')
        print "wrote page",page_num,"of", artist
        page_num += 1






## Perhaps I don't need this damn webdriver anyway.
#
# driver = webdriver.Chrome()
# for artist in artists:
#     page_num = 0
#     while (True):
#
#
#         driver.get(artist_url(artist,page_num))
#         # time.sleep(3) # Let the user actually see something!
#         html_source = driver.page_source
#         if (len(html_source) < 8000):
#             break
#         tab_links += scraper.get_song_urls(html_source)
#         for tab in tab_links:
#             tab_file.write(tab + '\n')
#         time.sleep(2) # Let the user actually see something!
#         print "wrote page",page_num,"of", artist
#         page_num += 1
#
# driver.quit()