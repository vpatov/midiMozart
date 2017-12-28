import httplib2
import scraper
import time
import threading
import Queue
import signal
import os
import re



http = httplib2.Http()
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
base_url = "https://www.ultimate-guitar.com"
artists = set([i.strip() for i in open('artists.txt','r').read().split('\n')])

def artist_url(band_name,page_num):
    return base_url + '/tabs/' + band_name.strip().replace(' ','_') + '_tabs' + str(page_num) + '.htm'

def get_tab_download_pages():
    tab_file = open('tab_links.txt','w')
    for artist in artists:
        page_num = 0
        while (True):
            try:
                status, response = http.request(artist_url(artist,page_num))
                if (len(response) < 8000):
                    break
                batch = scraper.get_tab_download_page_links(response)

                for tab in batch:
                    tab_file.write(tab[0] +',' + tab[1] + ',' + artist + '\n')
                print "wrote page",page_num,"of", artist
                page_num += 1
            except Exception as e:
                print e
                tab_file.close()

    tab_file.close()

def download_tabs():
    tabs_to_download = open('tab_download_links.txt')
    for line in tabs_to_download:
        parts = line.split(',')
        link = parts[0]
        if link == 'broken':
            continue
        name = parts[1]
        page_link = parts[2]
        artist = parts[3]
        filename = 'tabs/' + artist.strip()+'-'+name
        try:
            f = open(filename,'r')
            f.close()
            print filename,'already downloaded'
        except IOError as e:
            print 'downloading',filename
            status, response = http.request(link)
            f = open(filename,'wb')
            f.write(response)
            f.close()
            time.sleep(4)





scraped = 0
def get_tab_download_links():
    global scraped
    #read the tab_download_page_links
    tab_file = open('tab_links.txt','r')
    tab_download_links_file = open('tab_download_links.txt','a')
    tab_download_pages = Queue.Queue()
    tab_download_pages_set = set()
    num_lines = 0
    for line in tab_file:
        num_lines += 1
        parts = line.split(',')
        tab_download_pages_set.add((parts[0].strip(),parts[1].strip(),parts[2].strip()))

    num_removed = 0
    #read the list of tab download pages already scraped
    tab_already_scraped_file = open('tab_download_links.txt','r')
    for line in tab_already_scraped_file:
        parts = line.split(',')

        name = parts[1].strip()
        link = parts[2].strip()
        artist = parts[3].strip()
        if ((link,name,artist) in tab_download_pages_set):
            tab_download_pages_set.remove((link,name,artist))
            num_removed += 1

    print "Already downloaded:",num_removed



    tab_download_links = Queue.Queue()

    for group in tab_download_pages_set:
        tab_download_pages.put(group)

    def get_tab_download_link():
        global scraped
        time.sleep(1)
        while (True):
            try:
                print 'trying'
                link,song_name,artist = tab_download_pages.get(timeout=10)
                status,response = http.request(link)
                download_link = scraper.get_tab_download_link(response)
                tab_download_links.put((download_link,song_name,link,artist))
                if (scraped % 10 == 0 and scraped != 0) or (scraped < 10):
                    print "Scraped",scraped,'...'
                scraped += 1

            except Exception as e:
                print e
                print "Should be done scraping!"
                exit()

    def write_tab_download_links():
        while (True):
            try:
                link,song_name,page_link,artist = tab_download_links.get(timeout=20)
                tab_download_links_file.write(link.strip() + ',' + song_name.strip() + ',' + page_link.strip() + ',' + artist + '\n')
            except Exception as e:
                print e
                print "Should be done writing!"
                tab_download_links_file.close()
                exit()

    def wrapup():
        print "wrapping up"
        tab_download_links_file.close()
        exit()

    signal.signal(signal.SIGINT, wrapup)
    signal.signal(signal.SIGTERM, wrapup)
    signal.signal(signal.SIGABRT, wrapup)

    #setup threads
    for i in range(0,1):
        t = threading.Thread(target=get_tab_download_link)
        t.start()
    t = threading.Thread(target=write_tab_download_links)
    t.start()



# get_tab_download_pages()
# get_tab_download_links()
download_tabs()



