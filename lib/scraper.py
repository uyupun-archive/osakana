from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from fastapi import Body
from requests.exceptions import HTTPError

from api.schemas.reading_list import ReadingListAddRequest


class WebPageScraper:
    def __init__(self, url: str):
        self.url = url

    def get_title(self) -> str:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except HTTPError as e:
            raise WebPageAccessError(e)

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title")
        if title:
            return title.text
        raise TitleNotFoundError("Title not found error")

    @classmethod
    def create_scraper(cls, req: ReadingListAddRequest=Body(...)) -> WebPageScraper:
        return cls(url=req.url)


class WebPageAccessError(Exception):
    def __init__(self, http_error: HTTPError) -> None:
        super().__init__(str(http_error))

        self.status_code = http_error.response.status_code
        self.message = str(http_error)


class TitleNotFoundError(Exception):
    pass
