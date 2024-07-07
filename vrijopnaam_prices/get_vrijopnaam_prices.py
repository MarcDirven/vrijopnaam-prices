import argparse
import json
import asyncio
import os
import sys

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
    json.dump(prices, sys.stdout, indent=args.indent, ensure_ascii=False)
    return 0


def start():
    return asyncio.run(main())


if __name__ == '__main__':
    exit(start())
