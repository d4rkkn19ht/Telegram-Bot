import requests
from bs4 import BeautifulSoup
import json
from Article import Article

baseUrl = "https://vnexpress.net/"

def GetNews(limit_news = 20): # Tạo biến limit_news để lấy số lượng tin mà mình cần thôi
    s = requests.Session() # Store sesstion lại
    response = s.get(baseUrl) # Thực hiện Get request
    soup = BeautifulSoup(response.content, 'html.parser') # Đưa vào biến soup chuẩn bị bóc tách dữ liệu
    article = soup.select("article.item-news", limit=limit_news) # Tách dữ liệu phần thẻ article ra

    listArticle = []
    for element in article:
        title = element.select("h3.title-news > a") # Lấy phần thẻ chứa title
        description = element.select("p.description > a") # Lấy phần thẻ chứa description
        for x in range(len(title)): # serialize object này lại thành json để lấy dữ liệu dễ dàng hơn
            listArticle.append(json.dumps(Article(title[x]['title'], title[x]['href'], description[x].text).__dict__, ensure_ascii=False))
    return listArticle

