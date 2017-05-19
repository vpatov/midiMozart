from bs4 import BeautifulSoup

def get_song_urls(artist_source):
    urls = []

    soup = BeautifulSoup(artist_source,'lxml')
    body = soup.find('body')
    tbodies = body.findAll('tbody')
    largest_tbody = tbodies[0]
    for tbody in tbodies:
        if len(tbody) > len(largest_tbody):
            largest_tbody = tbody

    for tr in largest_tbody.findAll('tr'):
        trs = tr.findAll('td')
        if (trs):
            typeoftab = trs[-1].text
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
        rating_count = int(rating_count)
        link = tr.find('a').get('href')
        song_name = tr.find('a').text

        if float(rating_td['title']) >= 4.0:
            urls.append((link,song_name))


    return urls


source = """<html>
	<thing1>
		<thing2>
		</thing2>

		<thing2>
			<thing3> some text </thing3>
		</thing2>

		<thing4>
			thing4 text
			<thing2>
				some more thing2 text
			</thing2>
		</thing4>



	</thing1>
</html>"""

# soup = BeautifulSoup(source,'lxml')
# print soup.find('thing1')