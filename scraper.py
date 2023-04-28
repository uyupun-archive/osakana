import requests
from bs4 import BeautifulSoup


url = "https://qiita.com/Tsutou/items/4fd498f8ab2638bd5650"

response = requests.get(url)

soup = BeautifulSoup(markup=response.content, features="html.parser")

title = soup.find("title").text

og_description = soup.find('meta', property='og:description')
if og_description:
    og_description = og_description.get('content')

keywords = soup.find('meta', attrs={'name': 'keywords'})
if keywords:
    keywords = keywords.get('content')

print("Title:", title)
print("og:description:", og_description)
print("Keywords:", keywords)
