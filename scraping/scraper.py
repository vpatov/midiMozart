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
        rating_td = tr.find('span',{'class':'rating'})
        if (not rating_td):
            continue
        link = tr.find('a').get('href')
        trs = tr.findAll('td')
        if (trs):
            typeoftab = trs[-1].text
        if float(rating_td['title']) > 4.0 and typeoftab.strip() == 'Guitar Pro':
            urls.append(link)


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