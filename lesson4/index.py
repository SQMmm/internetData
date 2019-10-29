import requests
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
mail_ru_link = "http://mail.ru"
lenta_link = "https://lenta.ru/"

req = requests.get(mail_ru_link, headers=headers).text
root = html.fromstring(req)

news = []

links = root.xpath(
    "//div[@class='tabs__content']/*/div[contains(@class, 'news-item')]/a[@name]/@href | "
    "//div[@class='tabs__content']/*/div[contains(@class, 'news-item')]/*/a[contains(@href, 'https://')]/@href")
titles = root.xpath("//div[@class='tabs__content']/*/div[contains(@class, 'news-item')]/a[@name]/*/*/h3/text() | "
                         "//div[@class='tabs__content']/*/div[contains(@class, 'news-item')]/*/a[contains(@href, 'https://')]/text()")
if len(links) > 0:
    for i, l in enumerate(links):
        article = {'link': l, 'title': titles[i], 'source': mail_ru_link}
        news.append(article)
else:
    print("Error")


req = requests.get(lenta_link, headers=headers).text
root = html.fromstring(req)

links = root.xpath(
    "//div[@class='item']/a/@href")
titles = root.xpath("//div[@class='item']/a/text()")
if len(links) > 0:
    for i, l in enumerate(links):
        article = {'link': lenta_link + l, 'title': titles[i], 'source': lenta_link}
        news.append(article)
else:
    print("Error")
print(news)