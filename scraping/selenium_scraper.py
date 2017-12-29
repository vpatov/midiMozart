from selenium import webdriver
import time
import os
import termcolor
import csv

user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
selenium_scraped_tabs_dir = '/home/vasia/repos/midiMozart/scraping/selenium_scraped_tabs'
all_tabs_dir = '/home/vasia/repos/midiMozart/scraping/tabs'

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', selenium_scraped_tabs_dir)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
profile.set_preference("general.useragent.override", user_agent)

browser = webdriver.Firefox(profile,
	executable_path='/home/vasia/.local/share/webdrivers/geckodriver')



def rename_dl_file(artist,song):
    files = os.listdir(selenium_scraped_tabs_dir)
    if (len(files) == 0):
        return False
    elif (len(files) > 1):
        print(termcolor.colored(files,"red"))
        raise Exception("Restart script - download is out of sync")
    file = os.path.join(selenium_scraped_tabs_dir,files[0])
    os.rename(file,os.path.join(all_tabs_dir,artist.strip()+'-'+song))
    return True




def download_tabs():
    tab_file = open('tab_links.txt','r')
    reader = csv.reader(tab_file)
    count_broken = 0
    count_lines = 0
    for line in reader:
        link,song,artist = line
        count_lines += 1
        print(termcolor.colored("%d:\t" % count_lines,"magenta"))
        if link == 'broken':
            count_broken += 1
            print(artist.strip() + '-' + song + " BROKEN LINK. %d" % count_broken)
            continue

        filename = 'tabs/' + artist.strip()+'-'+song
        if (os.path.isfile(filename)):
            print(termcolor.colored('Already Downloaded: %s' % filename,"yellow"))
        else:
            print(termcolor.colored('Downloading:\t%s' % artist.strip()+'-'+song, "cyan"))
            browser.get(link)
            try:
                browser.find_element_by_class_name('prosubmit').click()
            except Exception as e:
                print(termcolor.colored(e,"red"))
                continue

            if (not rename_dl_file(artist,song)):
                print(termcolor.colored("Waiting for download: %s-%s... " % (artist,song),"yellow"),end='')
                wait_time = 1
                while(not rename_dl_file(artist,song)):
                    print(termcolor.colored("%d " % wait_time,"yellow",attrs=['bold']),end='')
                    wait_time += 1
                    time.sleep(1)
                
            print(termcolor.colored("Downloaded\t%s-%s" % (artist,song),"blue",attrs=['bold']))
            time.sleep(3)



download_tabs()