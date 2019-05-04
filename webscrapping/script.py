import requests
from bs4 import BeautifulSoup

bURL = "https://www.prothomalo.com"
fileName = "prothom.txt"
r=requests.get(bURL+"/education")
c=r.content

links = []
scrap = []

soup=BeautifulSoup(c, "html.parser")
f = soup.find("div",{"id":"div_53194"}).find("a")
links.append(f["href"])

f2 =soup.find("div",{"id":"div_53195"}).find_all("a")

for item in f2:
    links.append(item["href"])

all=soup.find_all("div",{"class":"col col4"})
for item in all:
    links.append(item.find("a")["href"])

for item in links:
    arr = item.split("/")
    file = open(fileName, "a+")
    if arr[3] not in open(fileName,"r").read():
        scrap.append(item)
        open(fileName,"a+").write(arr[3] + "\n")

for item in scrap:
    r = requests.get(bURL + item)
    c = r.content

    soup = BeautifulSoup(c, "html.parser")
    title = soup.find("h1", {"class": "title mb10"}).text
    article = soup.find("article")
    image = article.find("img")["src"] if article.find("img") else None
    pAll = article.find_all("p")

    print(title)
    print(image)
    for p in pAll:
        print(p.text)
    print("\n")
