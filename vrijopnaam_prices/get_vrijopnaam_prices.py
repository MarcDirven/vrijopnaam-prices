import argparse
from vrijopnaam_prices.vrijopnaam_prices import get_prices
from vrijopnaam_prices.vrijopnaam import VrijOpNaam
import json
import os
import asyncio


async def main():
    p = argparse.ArgumentParser()
    p.add_argument('--username', required=False, type=str, default=os.getenv(VrijOpNaam.VRIJOPNAAM_USERNAME))
    p.add_argument('--password', required=False, type=str, default=os.getenv(VrijOpNaam.VRIJOPNAAM_PASSWORD))
    p.add_argument('--pretty-output', action='store_true')
    p.add_argument('--electricity-prices', action='store_true')
    p.add_argument('--gas-prices', action='store_true')
    args = p.parse_args()
    prices = (await get_prices(args.username, args.password, args.gas_prices, args.electricity_prices)).to_json()
    pretty_json = json.dumps(prices, indent=4 if args.pretty_output else None, ensure_ascii=False).encode('utf8')
    print(pretty_json.decode())


def start():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()


if __name__ == '__main__':
    start()
