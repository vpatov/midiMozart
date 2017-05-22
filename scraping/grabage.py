# f = open('metalcore_artists.txt')
#
# contents = f.read()
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(contents,'lxml')
# tds = soup.find_all('td')
# bands = []
# for td in tds:
#     x = td.find('a')
#     if (x):
#         y = x.get('title')
#         if (y):
#             if '(band)' in y:
#                 bands.append(y[:y.index('(band)')].strip())
#
# for b in bands:
#     print b

f = open('tab_links.txt','r')
p = set()
for line in f:
    parts = line.split()
    p.add((parts[0].strip(),parts[1].strip()))

print len(p)