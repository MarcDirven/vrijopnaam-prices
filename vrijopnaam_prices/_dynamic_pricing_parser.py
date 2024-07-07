from typing import Iterable
import asyncio
import bs4

from vrijopnaam_prices._vrijopnaam import VrijOpNaam
from vrijopnaam_prices.dynamic_prices import DynamicElectricityPrices, DynamicGasPrices, DynamicPrices


def parse_price(html: str) -> DynamicPrices:
    table = bs4.BeautifulSoup(html, features='html.parser')
    pricing_table = table.find('table', class_=VrijOpNaam.PRICING_TABLE)
    if not pricing_table:
        raise RuntimeError(f'Table with class "{VrijOpNaam.PRICING_TABLE}" was not found')

    result = table.find('title')
    if result and VrijOpNaam.GAS in result.text:
        return DynamicGasPrices(pricing_table)
    elif result and VrijOpNaam.ELECTRICITY in result.text:
        return DynamicElectricityPrices(pricing_table)
    raise RuntimeError('There was no table found with a title')


async def parse_prices(htmls: Iterable) -> DynamicPrices:
    dynamic_prices = DynamicPrices()
    results = await asyncio.gather(*(asyncio.to_thread(parse_price, html) for html in htmls))
    dynamic_prices.add(results)
    return dynamic_prices
