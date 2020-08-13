from bs4 import BeautifulSoup
import requests

def get_news():
    res = requests.get("https://www.itmedia.co.jp/")
    soup = BeautifulSoup(res.text,"html.parser")

    content = soup.find("div",{"class":"colBoxOuter"})
    news = content.find("div",{"class":"colBoxTitle"}).find("h3").find("a").get("href")
    
    """
    news = [t.find("h3").find("a").get("href") for t in content.find_all("div",{"class":"colBoxTitle"})]
    news = [soup.find("h3").find("a").get("href")]
    """

    return news