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

def get_news_list():
    res = requests.get("https://www.itmedia.co.jp/")
    soup = BeautifulSoup(res.text,"html.parser")

    content = soup.find("div",{"class":"colBoxOuter"})
    
    news = [t.find("h3").find("a").get("href") for t in content.find_all("div",{"class":"colBoxTitle"})]
    #news = [soup.find("h3").find("a").get("href")]

    return news

def filter_search(news):

    req = requests.get(news)
    req.encoding = "shift_jis"

    soup = BeautifulSoup(req.text,"html.parser")

    for script in soup(["script", "style"]):
        script.decompose()

    content = soup.get_text()
    content = content.replace('\n',"")

    return content

def compare_words(yourmentions,news):
    for word in yourmentions:
        if word in news:
            return 1

    return 0

