from bs4 import BeautifulSoup
import requests
print("บางแสน")
url = "http://www.pattayaconcierge.com/rent-space/bangsaen/"
html  = requests.get(url).content
soup = BeautifulSoup(html, "html.parser")
chonburi = soup.find_all('a', {'target' : "_blank" , 'style' : "font-weight:bold;"})
for nav in chonburi:
    url_chonburi =  nav['href']
    print(url_chonburi)
    new_html = requests.get(url_chonburi).content
    new_soup = BeautifulSoup(new_html, "html.parser")
    print(new_soup)