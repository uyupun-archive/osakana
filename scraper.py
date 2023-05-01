from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from fastapi import Body

from api.schemas.reading_list import ReadingListAddRequest


class WebPageScraper:
    def __init__(self, url: str):
        self.url = url

    def get_title(self) -> str:
        response = requests.get(self.url)
        if response.status_code != 200:
            raise WebPageAccessError

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title")
        if title:
            return title.text
        raise TitleNotFoundError

    @classmethod
    def create_scraper(cls, req: ReadingListAddRequest=Body(...)) -> WebPageScraper:
        return cls(url=req.url)


class WebPageAccessError(Exception):
    pass


class TitleNotFoundError(Exception):
    pass


# og_description = soup.find('meta', property='og:description')
# if og_description:
#     og_description = og_description.get('content')

# keywords = soup.find('meta', attrs={'name': 'keywords'})
# if keywords:
#     keywords = keywords.get('content')

# print("og:description:", og_description)
# print("Keywords:", keywords)
