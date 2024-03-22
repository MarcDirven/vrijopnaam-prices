import os
import json

import asyncio
import argparse
import dynamic_pricing_parser as parser
from vrijopnaam import VrijOpNaam
from vrijopnaam_session import VrijOpNaamSession


async def get_prices(username: str, password: str, gas_price: bool = True, electricity_price: bool = True):
    async with VrijOpNaamSession(username, password) as session:
        await session.login()
        htmls = await session.scrape_prices(gas_price, electricity_price)
    return parser.parse_prices(htmls)


async def __run_main():
    p = argparse.ArgumentParser()
    p.add_argument('--username', required=False, type=str, default=os.getenv(VrijOpNaam.VRIJOPNAAM_USERNAME))
    p.add_argument('--password', required=False, type=str, default=os.getenv(VrijOpNaam.VRIJOPNAAM_PASSWORD))
    p.add_argument('--pretty-output', action='store_true')
    p.add_argument('--electricity-price', action='store_true')
    p.add_argument('--gas-price', action='store_true')
    args = p.parse_args()
    prices = (await get_prices(args.username, args.password)).to_json()
    pretty_json = json.dumps(prices, indent=4 if args.pretty_output else None, ensure_ascii=False).encode('utf8')
    print(pretty_json.decode())


if __name__ == '__main__':
    asyncio.run(__run_main())
