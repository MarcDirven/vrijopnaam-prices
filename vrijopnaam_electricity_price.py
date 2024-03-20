import os
import json

import bs4
import aiohttp
import asyncio
import argparse
import dynamic_pricing_parser as parser
from vrijopnaam import VrijOpNaam


def get_csrf_middleware_token(html: str) -> str:
    return bs4.BeautifulSoup(html, features='html.parser').html['data-csrf-token']


async def get_prices(username: str, password: str, gas_price: bool = True, electricity_price: bool = True):
    async with aiohttp.ClientSession() as session:
        body = {VrijOpNaam.USERNAME: username, VrijOpNaam.PASSWORD: password}

        async with session.get(VrijOpNaam.URL) as resp_1:
            html = await resp_1.text()
            body[VrijOpNaam.CSRF_TOKEN] = get_csrf_middleware_token(html)
            url = str(resp_1.real_url)

        if 'sessionid' in resp_1.cookies:
            resp_1.cookies.pop('sessionid')

        async with session.post(url, cookies=resp_1.cookies, data=body, headers={'Referer': url}) as resp_2:
            html = await resp_2.text()
            url = str(resp_2.real_url)
            body = {
                VrijOpNaam.CSRF_TOKEN: get_csrf_middleware_token(html),
                VrijOpNaam.STAY_SIGNED_IN_BTN: VrijOpNaam.YES,
                VrijOpNaam.ASK_STAY_SIGNED_IN: VrijOpNaam.ON
            }

        async with session.post(
                url, cookies=resp_2.cookies, data=body, headers={'Referer': url}) as resp_3:
            html = await resp_3.text()
            body[VrijOpNaam.CSRF_TOKEN] = get_csrf_middleware_token(html)
            url = str(resp_3.real_url).removesuffix('/')

        if electricity_price:
            async with session.get(f'{url}/{VrijOpNaam.PRICING_ELECTRICITY}/', cookies=resp_3.cookies, data=body,
                                   headers={'Referer': url}) as resp_4:
                html = await resp_4.text()
                return parser.parse_prices(html)

        if gas_price:
            pass


async def __run_main():
    p = argparse.ArgumentParser()
    p.add_argument('--username', required=True, type=str)
    p.add_argument('--password', required=False, type=str, default=os.getenv(VrijOpNaam.VRIJOPNAAM_PASSWORD))
    p.add_argument('--pretty-output', action='store_true')
    p.add_argument('--electricity-price', action='store_true')
    p.add_argument('--gas-price', action='store_true')
    args = p.parse_args()
    prices = (await get_prices(args.username, args.password, gas_price=False)).to_json()
    pretty_json = json.dumps(prices, indent=4 if args.pretty_output else None, ensure_ascii=False).encode('utf8')
    print(pretty_json.decode())


if __name__ == '__main__':
    asyncio.run(__run_main())
