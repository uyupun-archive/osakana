from __future__ import annotations
import sys
from urllib.parse import urljoin

import cchardet
import requests
from bs4 import BeautifulSoup, Tag
from fastapi import Body
from requests import Response
from requests.exceptions import HTTPError
from typing import Type


class WebPageScraper:
    def __init__(self):
        self._res = None
        self._soup = None

    def fetch(self, url: str, parser: Type[BeautifulSoup] = BeautifulSoup) -> None:
        self._res = self._get(url=url)
        self._soup = parser(self._res.text, "html.parser")

    def _get(self, url: str) -> Response:
        try:
            res = requests.get(url=url)
            res.raise_for_status()
        except HTTPError as e:
            raise WebPageAccessError(e)
        res = self._guess_encoding(res=res)
        return res

    def _guess_encoding(self, res: Response) -> Response:
        encoding = cchardet.detect(res.content)["encoding"]
        res.encoding = encoding
        return res

    def get_title(self) -> str:
        if not self._soup:
            raise BeautifulSoupEmptyError()

        title = self._soup.find("title")
        if title:
            return title.text
        raise TitleNotFoundError("Title not found error")

    def get_favicon_link(self) -> str:
        favicon_link = self._get_icon_element()["href"]
        if not isinstance(favicon_link, str):
            raise FaviconNotFoundError("Favicon not found error")

        if not favicon_link.startswith("http"):
            favicon_link = urljoin(url, favicon_link)
        return favicon_link

    def _get_icon_element(self) -> Tag:
        if not self._soup:
            raise BeautifulSoupEmptyError()

        icon_link = self._soup.find("link", rel=["icon", "shortcut icon"])
        if (not icon_link) or (not isinstance(icon_link, Tag)) or (not icon_link.has_attr("href")):
            raise IconNotFoundError("Icon not found error")
        return icon_link

    @classmethod
    def create_scraper(cls) -> WebPageScraper:
        return cls()


class WebPageAccessError(Exception):
    def __init__(self, http_error: HTTPError) -> None:
        super().__init__(str(http_error))

        self.status_code = http_error.response.status_code
        self.message = str(http_error)


class TitleNotFoundError(Exception):
    pass


class BeautifulSoupEmptyError(Exception):
    pass


class IconNotFoundError(Exception):
    pass


class FaviconNotFoundError(Exception):
    pass


if __name__ == "__main__":
    url = sys.argv[1]
    scraper = WebPageScraper()
    scraper.fetch(url=url)

    title = scraper.get_title()
    print("Title:", title)

    favicon_link = scraper.get_favicon_link()
    print("Favicon link:", favicon_link)
