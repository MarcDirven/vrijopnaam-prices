import argparse
import asyncio
import json
import os

from vrijopnaam_prices._vrijopnaam import VrijOpNaam
from vrijopnaam_prices.prices import get_prices


async def main():
    p = argparse.ArgumentParser()
    p.add_argument('--username', '-u', required=False, type=str, default=os.getenv(VrijOpNaam.VRIJOPNAAM_USERNAME))
    p.add_argument('--password', '-p', required=False, type=str, default=os.getenv(VrijOpNaam.VRIJOPNAAM_PASSWORD))
    p.add_argument('--indent', '-i', type=int, required=False, default=None)
    p.add_argument('--electricity-prices', '-e', action='store_true')
    p.add_argument('--gas-prices', '-g', action='store_true')
    args = p.parse_args()

    if not args.gas_prices and not args.electricity_prices:
        args.gas_prices, args.electricity_prices = True, True

    prices = (await get_prices(args.username, args.password, args.gas_prices, args.electricity_prices)).to_json()
    pretty_json = json.dumps(prices, indent=args.indent, ensure_ascii=False).encode('utf8')
    print(pretty_json.decode())


def start():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()


if __name__ == '__main__':
    start()
