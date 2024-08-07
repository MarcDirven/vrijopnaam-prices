import asyncio
import re
from typing import Iterable

import aiohttp

from vrijopnaam_prices._vrijopnaam import VrijOpNaam


async def _get_csrf_middleware_token(response: aiohttp.ClientResponse) -> str:
    while not response.content.at_eof():
        line = str(await response.content.readline())
        m = re.search(r'(?<=data-csrf-token=")[^"^\']*', line)
        if m:
            return m.group()
    raise RuntimeError('No property found with name "data-csrf-token"')


async def _fetch(url: str, session: aiohttp.ClientSession, **kwargs):
    async with session.get(url, **kwargs) as r:
        return await r.text()


class ConditionalFetch:
    def __init__(self, do_fetch: bool, url: str):
        self.__fetch = do_fetch
        self.__url = url

    def __get_url(self):
        return self.__url

    def __condition(self):
        return self.__fetch

    url = property(fget=__get_url)
    condition = property(fget=__condition)


class VrijOpNaamSession:
    def __init__(self, username: str, password: str):
        self.__session = aiohttp.ClientSession()
        self.__body = {VrijOpNaam.USERNAME: username, VrijOpNaam.PASSWORD: password}
        self.__url = ''
        self.__cookies = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    async def close(self):
        if not self.__session.closed:
            await self.__session.close()

    async def __main_page(self):
        async with self.__session.get(VrijOpNaam.URL) as resp_1:
            self.__body[VrijOpNaam.CSRF_TOKEN] = await _get_csrf_middleware_token(resp_1)
            self.__url = str(resp_1.real_url)
            self.__cookies = resp_1.cookies

        if VrijOpNaam.SESSION_ID in self.__cookies:
            self.__cookies.pop(VrijOpNaam.SESSION_ID)

    async def __login(self):
        async with self.__session.post(
                self.__url, cookies=self.__cookies, data=self.__body, headers={'Referer': self.__url}) as resp_2:
            self.__url = str(resp_2.real_url)
            self.__cookies = resp_2.cookies
            self.__body = {
                VrijOpNaam.CSRF_TOKEN: await _get_csrf_middleware_token(resp_2),
                VrijOpNaam.STAY_SIGNED_IN_BTN: VrijOpNaam.YES,
                VrijOpNaam.ASK_STAY_SIGNED_IN: VrijOpNaam.ON
            }

    async def __stay_signed_in(self):
        async with self.__session.post(
                self.__url, cookies=self.__cookies, data=self.__body, headers={'Referer': self.__url}) as resp_3:
            self.__body[VrijOpNaam.CSRF_TOKEN] = await _get_csrf_middleware_token(resp_3)
            self.__url = str(resp_3.real_url).removesuffix('/')
            self.__cookies = resp_3.cookies

    async def login(self):
        await self.__main_page()
        await self.__login()
        await self.__stay_signed_in()

    def scrape_prices(self, price_fetchers: Iterable[ConditionalFetch]) -> asyncio.Future[Iterable]:
        urls = (f'{self.__url}/{pf.url}' for pf in price_fetchers if pf.condition)
        tasks = [
            _fetch(url, self.__session, cookies=self.__cookies, data=self.__body, headers={'Referer': url}) for url in urls
        ]
        return asyncio.gather(*tasks)
