import bs4
import requests
def main(search = ""):
    search = search + " :imdb"
    r = requests.get("https://duckduckgo.com/html/",data={"q":search})
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    links = soup.find_all("a",attrs={"class":u"result__a"},href=True)
    for l in links:
        print(l["href"])
        print("####")
if __name__ == '__main__':
    main(input("Search ?>"))
